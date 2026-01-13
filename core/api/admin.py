from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Project, Document, History

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_staff', 'created_at')
    search_fields = ('email', 'username')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at')
    list_filter = ('created_at', 'owner')
    search_fields = ('title', 'description')
    raw_id_fields = ('owner',)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('project', 'last_modified')
    search_fields = ('project__title', 'content')
    raw_id_fields = ('project',)

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('document', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('document__project__title', 'content_snapshot')
    raw_id_fields = ('document',)