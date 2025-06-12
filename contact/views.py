from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ContactSubmissionSerializer
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def submit_contact_form(request):
    logger.info(f"Contact form submission received from IP: {request.META.get('REMOTE_ADDR', 'Unknown')}")
    logger.info(f"Request data: {request.data}")
    
    try:
        serializer = ContactSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            submission = serializer.save()
            logger.info(f"Contact submission saved: {submission.id}")
            
            # Prepare email content
            subject = f'New Contact Form Submission from {submission.first_name} {submission.last_name}'
            message = f"""
            New contact form submission received:
            
            Name: {submission.first_name} {submission.last_name}
            Email: {submission.email_address}
            Phone: {submission.phone}
            
            Message:
            {submission.message}
            
            Submission ID: {submission.id}
            Timestamp: {submission.created_at}
            """
            
            try:
                logger.info(f"Attempting to send email to: {settings.CONTACT_FORM_EMAIL}")
                logger.info(f"From email: {settings.DEFAULT_FROM_EMAIL}")
                logger.info(f"Email backend: {settings.EMAIL_BACKEND}")
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_FORM_EMAIL],
                    fail_silently=False,
                )
                logger.info("Contact form email sent successfully")
                
            except Exception as e:
                logger.error(f"Failed to send email notification: {str(e)}")
                logger.error(f"Email error type: {type(e).__name__}")
                # Continue execution - we don't want to fail the submission just because email failed

            return Response({
                'status': 'success',
                'message': 'Thank you for your message. We will get back to you soon.',
                'submission_id': submission.id
            }, status=status.HTTP_201_CREATED)
        
        else:
            logger.warning(f"Contact form validation failed: {serializer.errors}")
            return Response({
                'status': 'error',
                'message': 'Invalid form data',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Error processing contact form: {str(e)}")
        return Response({
            'status': 'error',
            'message': 'An unexpected error occurred. Please try again later.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
