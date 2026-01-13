from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Project, Document, History, User
from .serializers import (
    UserSerializer, ProjectSerializer, 
    DocumentSerializer, HistorySerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import BasePermission

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
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        # Create a document automatically when project is created
        Document.objects.create(project=project, content="")
        return project
    
    @action(detail=True, methods=['get'])
    def document(self, request, pk=None):
        project = self.get_object()
        try:
            document = Document.objects.get(project=project)
        except Document.DoesNotExist:
            document = Document.objects.create(project=project, content="")
        serializer = DocumentSerializer(document)
        return Response(serializer.data)
    
    @document.mapping.put
    def update_document(self, request, pk=None):
        project = self.get_object()
        try:
            document = Document.objects.get(project=project)
        except Document.DoesNotExist:
            document = Document.objects.create(project=project, content="")
        
        # Save current content to history before updating
        if document.content:
            History.objects.create(
                document=document,
                content_snapshot=document.content
            )
        
        serializer = DocumentSerializer(document, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Document.objects.filter(project__owner=self.request.user)
    
    def update(self, request, *args, **kwargs):
        document = self.get_object()
        
        # Save to history before updating
        if document.content:
            History.objects.create(
                document=document,
                content_snapshot=document.content
            )
        
        return super().update(request, *args, **kwargs)

class HistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        document_id = self.kwargs.get('document_id')
        return History.objects.filter(document_id=document_id)