from .views import ChatView
from django.urls import path


urlpatterns = [
    path('chat/<str:document_id>/', ChatView.as_view(), name="chat"),
] 