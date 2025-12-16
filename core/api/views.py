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
        return Response([{"id": p.id, "title": p.title} for p in projects])

    def post(self, request):
        project = Project.objects.create(
            owner=request.user,
            title=request.data['title'],
            description=request.data.get('description', '')
        )
        return Response({"id": project.id})

class DocumentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        doc, _ = Document.objects.get_or_create(project_id=project_id)
        return Response({"content": doc.content})

    def put(self, request, project_id):
        doc, _ = Document.objects.get_or_create(project_id=project_id)

        History.objects.create(
            document=doc,
            content_snapshot=doc.content
        )

        doc.content = request.data['content']
        doc.save()
        return Response({"message": "Saved"})

class HistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, document_id):
        history = History.objects.filter(document_id=document_id)
        return Response([
            {"content": h.content_snapshot, "timestamp": h.timestamp}
            for h in history
        ])
