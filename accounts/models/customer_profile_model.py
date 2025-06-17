from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # Link to Django's built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    phone_number = models.CharField(
        max_length=15,
        help_text="Required for order confirmations and delivery"
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text="Optional, useful for marketing and age verification"
    )
    
    class GenderChoices(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        OTHER = 'O', 'Other'
        PREFER_NOT_TO_SAY = 'N', 'Prefer not to say'

    gender = models.CharField(
        max_length=1,
        choices=GenderChoices.choices,
        null=True,
        blank=True,
        help_text="Optional, for personalized recommendations"
    )

    phone_verified = models.BooleanField(
        default=False,
        help_text="Boolean for SMS notifications"
    )

    def __str__(self):
        return f"UserProfile: {self.phone_number}"
