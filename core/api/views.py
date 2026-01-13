from rest_framework import viewsets, status, generics, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from .models import Project, Document, History, User
from .serializers import (
    UserSerializer, ProjectSerializer, 
    DocumentSerializer, HistorySerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import BasePermission
from rest_framework.pagination import PageNumberPagination
import datetime
from django.http import HttpResponse
import markdown

class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'project'):
            return obj.project.owner == request.user
        return False

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Registration successful!'
        }, status=status.HTTP_201_CREATED)

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Project.objects.filter(owner=self.request.user)
        
        # Filter by date
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if date_from:
            try:
                date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d').date()
                queryset = queryset.filter(created_at__date__gte=date_from)
            except ValueError:
                pass
        
        if date_to:
            try:
                date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d').date()
                queryset = queryset.filter(created_at__date__lte=date_to)
            except ValueError:
                pass
        
        return queryset
    
    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        # Create a document automatically when project is created
        Document.objects.create(project=project, content="# New Document\n\nStart writing here...")
        return project
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        project_title = instance.title
        self.perform_destroy(instance)
        return Response({
            'message': f'Project "{project_title}" has been deleted successfully.'
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        project = self.get_object()
        document = get_object_or_404(Document, project=project)
        
        content = document.content or ""
        words = len(content.split())
        characters = len(content)
        lines = content.count('\n') + 1
        history_count = History.objects.filter(document=document).count()
        
        return Response({
            'project_id': project.id,
            'title': project.title,
            'stats': {
                'words': words,
                'characters': characters,
                'lines': lines,
                'history_versions': history_count,
                'last_modified': document.last_modified
            }
        })
    
    @action(detail=True, methods=['get'])
    def document(self, request, pk=None):
        project = self.get_object()
        try:
            document = Document.objects.get(project=project)
        except Document.DoesNotExist:
            document = Document.objects.create(project=project, content="# New Document\n\nStart writing here...")
        
        serializer = DocumentSerializer(document)
        return Response(serializer.data)
    
    @document.mapping.put
    def update_document(self, request, pk=None):
        project = self.get_object()
        try:
            document = Document.objects.get(project=project)
        except Document.DoesNotExist:
            document = Document.objects.create(project=project, content="")
        
        # Save current content to history before updating (if content changed)
        if document.content != request.data.get('content', ''):
            History.objects.create(
                document=document,
                content_snapshot=document.content
            )
        
        serializer = DocumentSerializer(document, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                **serializer.data,
                'message': 'Document saved successfully!',
                'saved_at': timezone.now()
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination
    
    def get_queryset(self):
        return Document.objects.filter(project__owner=self.request.user)
    
    def update(self, request, *args, **kwargs):
        document = self.get_object()
        
        # Save to history before updating (only if content changed)
        if document.content != request.data.get('content', ''):
            History.objects.create(
                document=document,
                content_snapshot=document.content
            )
        
        return super().update(request, *args, **kwargs)

class HistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination
    
    def get_queryset(self):
        document_id = self.kwargs.get('document_id')
        document = get_object_or_404(Document, id=document_id, project__owner=self.request.user)
        return History.objects.filter(document=document).order_by('-timestamp')
    
    @action(detail=False, methods=['get'])
    def recent(self, request, document_id=None):
        """Get recent history (last 5 entries)"""
        document = get_object_or_404(Document, id=document_id, project__owner=self.request.user)
        recent_history = History.objects.filter(document=document).order_by('-timestamp')[:5]
        serializer = self.get_serializer(recent_history, many=True)
        return Response(serializer.data)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        # Don't allow password update through this endpoint
        if 'password' in request.data:
            return Response(
                {'error': 'Use the password change endpoint to update password.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)

# search endpoints
class SearchView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        
        # Search in projects
        projects = Project.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            owner=request.user
        )
        
        # Search in documents
        documents = Document.objects.filter(
            Q(content__icontains=query),
            project__owner=request.user
        )
        
        return Response({
            'projects': ProjectSerializer(projects, many=True).data,
            'documents': DocumentSerializer(documents, many=True).data
        })
    
# Add export functionality
class ExportView(APIView):
    def get(self, request, document_id):
        document = get_object_or_404(Document, id=document_id)
        format = request.GET.get('format', 'txt')
        
        if format == 'html':
            html_content = markdown.markdown(document.content)
            response = HttpResponse(html_content, content_type='text/html')
            response['Content-Disposition'] = f'attachment; filename="{document.project.title}.html"'
        elif format == 'pdf':
            # Use reportlab or weasyprint
            pass
        else:
            response = HttpResponse(document.content, content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename="{document.project.title}.txt"'
        
        return response
class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Basic analytics
        total_projects = Project.objects.filter(owner=user).count()
        total_documents = Document.objects.filter(project__owner=user).count()
        total_history = History.objects.filter(document__project__owner=user).count()
        
        # Recent activity
        recent_projects = Project.objects.filter(owner=user).order_by('-created_at')[:5]
        recent_history = History.objects.filter(
            document__project__owner=user
        ).order_by('-timestamp')[:10]
        
        # Document stats
        documents = Document.objects.filter(project__owner=user)
        total_words = sum(len(doc.content.split()) for doc in documents)
        total_chars = sum(len(doc.content) for doc in documents)
        
        return Response({
            'user': {
                'email': user.email,
                'username': user.username,
                'joined': user.created_at
            },
            'stats': {
                'total_projects': total_projects,
                'total_documents': total_documents,
                'total_history_versions': total_history,
                'total_words': total_words,
                'total_characters': total_chars
            },
            'recent_projects': ProjectSerializer(recent_projects, many=True).data,
            'recent_activity': HistorySerializer(recent_history, many=True).data
        })