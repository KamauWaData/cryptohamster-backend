from rest_framework import serializers
from .models import NewsletterSubscriber

class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['id', 'email', 'preferences', 'status', 'subscription_date', 'unsubscribe_token', 'created_at', 'updated_at']
        read_only_fields = ['id', 'subscription_date', 'unsubscribe_token', 'created_at', 'updated_at']