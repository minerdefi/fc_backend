from django.apps import AppConfig

class ContactConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contact'
    path = 'contact'  # Explicitly set the path
    
    def ready(self):
        # Import signal handlers
        import contact.signals
