from django.db import models

from common.models import BaseModel


class Notification(BaseModel):
    to_user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='notification_to_user',
    )
    title = models.CharField(max_length=255)
    descriptions = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'notifications'
        ordering = ('-created_at',)
