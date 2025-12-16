from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Project, Document, History

class RegisterView(APIView):
    def post(self, request):
        User.objects.create_user(
            username=request.data['email'],
            email=request.data['email'],
            password=request.data['password']
        )
        return Response({"message": "User created"})

class ProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Project.objects.filter(owner=request.user)
        return Response([
            {
                "id": p.id,
                "title": p.title,
                "description": p.description
            } for p in projects
        ])

    def post(self, request):
        if not request.data.get("title"):
            return Response(
                {"error": "Title is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        project = Project.objects.create(
            owner=request.user,
            title=request.data["title"],
            description=request.data.get("description", "")
        )
        return Response({"id": project.id}, status=status.HTTP_201_CREATED)
class DocumentView(APIView):
    permission_classes = [IsAuthenticated]

    def get_project(self, project_id, user):
        return get_object_or_404(Project, id=project_id, owner=user)

    def get(self, request, project_id):
        project = self.get_project(project_id, request.user)
        doc, _ = Document.objects.get_or_create(project=project)
        return Response({"content": doc.content})

    def put(self, request, project_id):
        project = self.get_project(project_id, request.user)
        doc, _ = Document.objects.get_or_create(project=project)

        History.objects.create(
            document=doc,
            content_snapshot=doc.content
        )

        doc.content = request.data.get("content", "")
        doc.save()

        return Response({"message": "Saved"})

class HistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, document_id):
        history = History.objects.filter(
            document_id=document_id
        ).order_by("-timestamp")[:10]

        return Response([
            {
                "content": h.content_snapshot,
                "timestamp": h.timestamp
            } for h in history
        ])

class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, project_id):
        project = get_object_or_404(
            Project, id=project_id, owner=request.user
        )

        project.title = request.data.get("title", project.title)
        project.description = request.data.get("description", project.description)
        project.save()

        return Response({"message": "Project updated"})

    def delete(self, request, project_id):
        project = get_object_or_404(
            Project, id=project_id, owner=request.user
        )
        project.delete()
        return Response({"message": "Project deleted"})

