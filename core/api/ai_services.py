from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'documents', views.DocumentViewSet, basename='document')

urlpatterns = [
    # Auth
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User
    path('user/profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
    
    # AI Endpoints
    path('ai/summarize/', views.AISummarizeView.as_view(), name='ai-summarize'),
    path('ai/rewrite/', views.AIRewriteView.as_view(), name='ai-rewrite'),
    path('ai/ideas/', views.AIIdeasView.as_view(), name='ai-ideas'),
    
    # History
    path('documents/<int:document_id>/history/', views.HistoryViewSet.as_view({'get': 'list'}), name='document-history'),
    path('documents/<int:document_id>/history/recent/', views.HistoryViewSet.as_view({'get': 'recent'}), name='recent-history'),
    
    # Include router URLs
    path('', include(router.urls)),
]