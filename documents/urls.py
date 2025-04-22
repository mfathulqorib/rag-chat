from django.urls import path
from .views import DocumentUploadView, QueryView

urlpatterns = [
    path('documents/', DocumentUploadView.as_view(), name="documents"),
    path('query/<str:id>/', QueryView.as_view(), name="query"),
] 