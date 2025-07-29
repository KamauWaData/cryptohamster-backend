from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import send_email
from django.conf import settings
from .models import NewsletterSubscriber
from .serializers import NewsletterSubscriberSerializer
from datetime import timezone, time


class NewsletterSubscribeView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email or '@' not in email:
            return Response({'error': 'Invalid email address'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            subscriber = NewsletterSubscriber.objects.filter(email=email.lower()).first()
            if subscriber:
                if subscriber.status == 'active':
                    return Response({'message': 'Email already subscribed'}, status=status.HTTP_200_OK)
                else:
                    subscriber.status = 'active'
                    subscriber.subscription_date = timezone.now()
                    subscriber.save()
                    return Response({'message': 'Subscription reactivated successfully'}, status=status.HTTP_200_OK)

            # Create new subscriber
            serializer = NewsletterSubscriberSerializer(data={'email': email.lower()})
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Successfully subscribed to newsletter'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NewsletterUnsubscribeView(APIView):
    def post(self, request):
        unsubscribe_token = request.data.get('unsubscribe_token')
        try:
            subscriber = NewsletterSubscriber.objects.get(unsubscribe_token=unsubscribe_token)
            subscriber.status = 'unsubscribed'
            subscriber.save()
            return Response({'detail': 'You have successfully unsubscribed.'}, status=status.HTTP_200_OK)
        except NewsletterSubscriber.DoesNotExist:
            return Response({'detail': 'Invalid unsubscribe token.'}, status=status.HTTP_400_BAD_REQUEST)

class SendWelcomeEmailView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email or '@' not in email:
            return Response({'error': 'Invalid email address'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            html_content = f"""
            <div style="max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif;">
              <div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); padding: 40px; text-align: center; color: white;">
                <h1 style="margin: 0; font-size: 32px; font-weight: bold;">
                  Trend<span style="color: #60a5fa;">Forge</span>
                </h1>
                <p style="margin: 10px 0 0; font-size: 18px; opacity: 0.9;">
                  Welcome to the future of tech insights
                </p>
              </div>
              
              <div style="padding: 40px; background: white;">
                <h2 style="color: #1e293b; margin-bottom: 20px;">Thanks for subscribing!</h2>
                <p style="color: #64748b; line-height: 1.6; margin-bottom: 20px;">
                  You're now part of our community of forward-thinking individuals who stay ahead of the curve in cryptocurrency, blockchain technology, and digital innovation.
                </p>
                <p style="color: #64748b; line-height: 1.6; margin-bottom: 30px;">
                  You'll receive our latest insights, breaking news, and expert analysis directly in your inbox.
                </p>
                
                <div style="text-align: center; margin: 30px 0;">
                  <a href="https://CryptoHamster.com" 
                     style="background: #3b82f6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block; font-weight: bold;">
                    Visit CryptoHamster
                  </a>
                </div>
                
                <p style="color: #94a3b8; font-size: 14px; margin-top: 30px;">
                  You can unsubscribe at any time by clicking the unsubscribe link in any of our emails.
                </p>
              </div>
              
              <div style="background: #f8fafc; padding: 20px; text-align: center; color: #64748b; font-size: 14px;">
                © {2023} CryptoHamster. All rights reserved.
              </div>
            </div>
            """
            send_email(email, "Welcome to CryptoHamster Newsletter!", html_content)
            return Response({'message': 'Welcome email sent successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class SendNewsletterView(APIView):
    def post(self, request):
        subject = request.data.get('subject')
        content = request.data.get('content')
        recipient_type = request.data.get('recipientType')  # 'active' or 'all'

        if not subject or not content or not recipient_type:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get subscribers based on recipient type
            if recipient_type == 'active':
                subscribers = NewsletterSubscriber.objects.filter(status='active')
            else:
                subscribers = NewsletterSubscriber.objects.all()

            if not subscribers.exists():
                return Response({'error': 'No subscribers found'}, status=status.HTTP_400_BAD_REQUEST)

            # Create email template with unsubscribe link
            def create_email_content(unsubscribe_token):
                return f"""
                <div style="max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif;">
                  <div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); padding: 20px; text-align: center; color: white;">
                    <h1 style="margin: 0; font-size: 24px; font-weight: bold;">
                      Trend<span style="color: #60a5fa;">Forge</span>
                    </h1>
                  </div>
                  
                  <div style="padding: 40px; background: white;">
                    {content}
                  </div>
                  
                  <div style="background: #f8fafc; padding: 20px; text-align: center; color: #64748b; font-size: 14px;">
                    <p>© {2023} TrendForge. All rights reserved.</p>
                    <p>
                      <a href="https://trendforge.com/unsubscribe?token={unsubscribe_token}" 
                         style="color: #3b82f6; text-decoration: none;">
                        Unsubscribe
                      </a>
                    </p>
                  </div>
                </div>
                """

            # Send emails in batches to avoid rate limits
            batch_size = 10
            success_count = 0
            error_count = 0

            for i in range(0, len(subscribers), batch_size):
                batch = subscribers[i:i + batch_size]
                for subscriber in batch:
                    try:
                        send_email(
                            to_email=subscriber.email,
                            subject=subject,
                            html_content=create_email_content(subscriber.unsubscribe_token)
                        )
                        success_count += 1
                    except Exception as e:
                        print(f"Failed to send to {subscriber.email}: {str(e)}")
                        error_count += 1

                # Add delay between batches
                if i + batch_size < len(subscribers):
                    time.sleep(1)

            return Response({
                'message': 'Newsletter sent successfully',
                'details': {
                    'total': len(subscribers),
                    'success': success_count,
                    'errors': error_count
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)