from django.urls import path
from .views import SendWelcomeEmailView, NewsletterSubscribeView, NewsletterUnsubscribeView, SendNewsletterView

urlpatterns = [
    path('send-welcome-email/', SendWelcomeEmailView.as_view(), name='send-welcome-email'),
    path('send-newsletter/', SendNewsletterView.as_view(), name='send-newsletter'),
     path('subscribe/', NewsletterSubscribeView.as_view(), name='newsletter-subscribe'),
    path('unsubscribe/', NewsletterUnsubscribeView.as_view(), name='newsletter-unsubscribe'),
]