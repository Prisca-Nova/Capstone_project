from django.urls import path
from .views import RegisterView, ProjectView, DocumentView, HistoryView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', TokenObtainPairView.as_view()),

    path('projects/', ProjectView.as_view()),
    path('projects/<int:project_id>/document/', DocumentView.as_view()),
    path('document/<int:document_id>/history/', HistoryView.as_view()),
]
