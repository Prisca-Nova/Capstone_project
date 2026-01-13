from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project, Document, History
from django.contrib.auth.password_validation import validate_password
import re

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'confirm_password', 'created_at')
        read_only_fields = ('created_at',)
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True}
        }
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()
    
    def validate_username(self, value):
        if not re.match(r'^[\w.@+-]+$', value):
            raise serializers.ValidationError(
                "Username can only contain letters, numbers, and @/./+/-/_ characters."
            )
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value
    
    def validate(self, data):
        if data['password'] != data.get('confirm_password', ''):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    document_count = serializers.SerializerMethodField()
    last_modified = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ('id', 'owner', 'title', 'description', 'created_at', 'document_count', 'last_modified')
        read_only_fields = ('owner', 'created_at')
    
    def get_document_count(self, obj):
        return obj.document.content.count('\n') + 1 if obj.document.content else 0
    
    def get_last_modified(self, obj):
        return obj.document.last_modified if hasattr(obj, 'document') and obj.document else None
    
    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        if len(value) > 200:
            raise serializers.ValidationError("Title cannot exceed 200 characters.")
        return value

class DocumentSerializer(serializers.ModelSerializer):
    project_title = serializers.ReadOnlyField(source='project.title')
    word_count = serializers.SerializerMethodField()
    character_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = ('id', 'project', 'project_title', 'content', 'last_modified', 'word_count', 'character_count')
        read_only_fields = ('project', 'last_modified', 'word_count', 'character_count')
    
    def get_word_count(self, obj):
        return len(obj.content.split()) if obj.content else 0
    
    def get_character_count(self, obj):
        return len(obj.content) if obj.content else 0

class HistorySerializer(serializers.ModelSerializer):
    formatted_time = serializers.SerializerMethodField()
    preview = serializers.SerializerMethodField()
    
    class Meta:
        model = History
        fields = ('id', 'document', 'content_snapshot', 'timestamp', 'formatted_time', 'preview')
        read_only_fields = ('timestamp', 'formatted_time', 'preview')
    
    def get_formatted_time(self, obj):
        from django.utils.timesince import timesince
        return f"{timesince(obj.timestamp)} ago"
    
    def get_preview(self, obj):
        preview = obj.content_snapshot[:100]
        if len(obj.content_snapshot) > 100:
            preview += "..."
        return preview