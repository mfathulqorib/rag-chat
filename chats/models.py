from django.db import models
from core.models import BaseModel
from documents.models import Document

class Chat(BaseModel):
    role = models.CharField(max_length=255)
    content = models.TextField()
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255)