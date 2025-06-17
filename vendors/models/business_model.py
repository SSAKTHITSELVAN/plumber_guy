from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.contrib.auth.models import User
import uuid
from django.conf import settings


class Business(models.Model):
    """
    Main business model for store registration
    """
    
    # Business Information
    BUSINESS_TYPE_CHOICES = [
        ('proprietor', 'Proprietor'),
        ('llp', 'Limited Liability Partnership'),
        ('pvt_ltd', 'Private Limited'),
        ('partnership', 'Partnership'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business_name = models.CharField(
        max_length=200, 
        help_text="Name of the business/shop"
    )
    business_type = models.CharField(
        max_length=20, 
        choices=BUSINESS_TYPE_CHOICES,
        help_text="Basic classification of business"
    )
    gstin = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        validators=[RegexValidator(
            regex=r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$',
            message='Invalid GSTIN format'
        )],
        help_text="GST Identification Number (optional for now)"
    )
    pan_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$',
            message='Invalid PAN format'
        )],
        help_text="PAN Card Number for financial verification"
    )
    
    # Primary Contact Information
    mobile_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message='Invalid mobile number format'
        )],
        help_text="Mobile number for OTP verification"
    )
    mobile_verified = models.BooleanField(default=False)
    email = models.EmailField(
        validators=[EmailValidator()],
        help_text="Email address for communication"
    )
    email_verified = models.BooleanField(default=False)
    
    # Business Address
    address_line1 = models.CharField(max_length=200)
    address_line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(
        max_length=6,
        validators=[RegexValidator(
            regex=r'^\d{6}$',
            message='Pincode must be 6 digits'
        )]
    )
    
    # Owner/Authorized Person
    owner_name = models.CharField(
        max_length=200,
        help_text="Full name of business owner"
    )
    aadhaar_number = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^\d{12}$',
            message='Aadhaar must be 12 digits'
        )],
        help_text="Aadhaar number (optional initially)"
    )
    
    # Product Information
    primary_categories = models.TextField(
        help_text="Primary product categories (comma-separated)"
    )
    brand_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Brand name or own label"
    )
    
    # Financial Information (Optional)
    bank_account_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Bank account number for payouts"
    )
    ifsc_code = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^[A-Z]{4}0[A-Z0-9]{6}$',
            message='Invalid IFSC code format'
        )],
        help_text="IFSC code for bank transfers"
    )
    account_holder_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Name as per bank account"
    )
    upi_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^[\w\.-]+@[\w\.-]+$',
            message='Invalid UPI ID format'
        )],
        help_text="UPI ID for payments"
    )
    
    # File Uploads (Optional)
    pan_certificate = models.FileField(
        upload_to='documents/pan/',
        blank=True,
        null=True,
        help_text="PAN certificate upload"
    )
    gst_certificate = models.FileField(
        upload_to='documents/gst/',
        blank=True,
        null=True,
        help_text="GST certificate upload"
    )
    business_logo = models.ImageField(
        upload_to='logos/',
        blank=True,
        null=True,
        help_text="Business logo for branding"
    )
    
    # Status and Verification
    VERIFICATION_STATUS = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS,
        default='pending'
    )
    verification_notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # ✅ Better than hardcoding accounts.User
        on_delete=models.CASCADE,
        related_name="shopkeeper_profile",  # 🔄 Optional but useful for reverse access
        help_text="Associated user account"
    )
    class Meta:
        verbose_name = "Business"
        verbose_name_plural = "Businesses"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.business_name} - {self.business_type}"