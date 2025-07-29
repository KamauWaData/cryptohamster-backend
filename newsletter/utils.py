import resend
from django.conf import settings

def send_email(to_email, subject, html_content):
    try:
        resend = resend(api_key=settings.RESEND_API_KEY)
        response = resend.emails.send(
            from_email="CryptoHamter <cryptohamstercloud@gmail.com>",
            to=[to_email],
            subject=subject,
            html=html_content,
        )
        return response
    except Exception as e:
        raise Exception(f"Error sending email: {str(e)}")