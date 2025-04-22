from django.db import models
from core.models import BaseModel

# Create your models here.

DOC_STATUS_PENDING = 'pending'
DOC_STATUS_PROCESSING = 'processing'
DOC_STATUS_COMPLETE = 'complete'

DOC_STATUS_CHOICES = (
    (DOC_STATUS_PENDING, 'pending'),
    (DOC_STATUS_PROCESSING, 'processing'),
    (DOC_STATUS_COMPLETE, 'complete')
)

class Document(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to='documents')

    raw_text = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=255, choices=DOC_STATUS_CHOICES, default=DOC_STATUS_PENDING)
