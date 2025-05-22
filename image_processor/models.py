from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Image(models.Model):
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
    )
    
    title = models.CharField(max_length=255)
    original_image = models.ImageField(upload_to='original/')
    compressed_image = models.ImageField(upload_to='compressed/', null=True, blank=True)
    compression_ratio = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
