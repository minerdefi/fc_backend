from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ContactSubmission
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=ContactSubmission)
def log_new_submission(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New contact submission received from {instance.first_name} {instance.last_name}")
