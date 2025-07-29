import uuid
from django.db import models


class NewsletterSubscriber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    preferences = models.JSONField(null=True, blank=True)  # Store preferences as JSON
    status = models.CharField(max_length=20, default='active')  # e.g., 'active', 'unsubscribed'
    subscription_date = models.DateTimeField(auto_now_add=True)
    unsubscribe_token = models.UUIDField(null=True, blank=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email