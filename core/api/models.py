from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Document(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    last_modified = models.DateTimeField(auto_now=True)

class History(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    content_snapshot = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
