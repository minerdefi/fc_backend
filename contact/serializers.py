from rest_framework import serializers
from .models import ContactSubmission

class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = ['first_name', 'last_name', 'email_address', 'phone', 'message']
        
    def validate_phone(self, value):
        # Basic phone validation - must be at least 10 digits
        digits = ''.join(filter(str.isdigit, value))
        if len(digits) < 10:
            raise serializers.ValidationError("Phone number must have at least 10 digits")
        return value
