# Generated by Django 5.2.1 on 2025-06-05 09:39

import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('business_name', models.CharField(help_text='Name of the business/shop', max_length=200)),
                ('business_type', models.CharField(choices=[('proprietor', 'Proprietor'), ('llp', 'Limited Liability Partnership'), ('pvt_ltd', 'Private Limited'), ('partnership', 'Partnership'), ('other', 'Other')], help_text='Basic classification of business', max_length=20)),
                ('gstin', models.CharField(blank=True, help_text='GST Identification Number (optional for now)', max_length=15, null=True, validators=[django.core.validators.RegexValidator(message='Invalid GSTIN format', regex='^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$')])),
                ('pan_number', models.CharField(blank=True, help_text='PAN Card Number for financial verification', max_length=10, null=True, validators=[django.core.validators.RegexValidator(message='Invalid PAN format', regex='^[A-Z]{5}[0-9]{4}[A-Z]{1}$')])),
                ('mobile_number', models.CharField(help_text='Mobile number for OTP verification', max_length=15, validators=[django.core.validators.RegexValidator(message='Invalid mobile number format', regex='^\\+?1?\\d{9,15}$')])),
                ('mobile_verified', models.BooleanField(default=False)),
                ('email', models.EmailField(help_text='Email address for communication', max_length=254, validators=[django.core.validators.EmailValidator()])),
                ('email_verified', models.BooleanField(default=False)),
                ('address_line1', models.CharField(max_length=200)),
                ('address_line2', models.CharField(blank=True, max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=6, validators=[django.core.validators.RegexValidator(message='Pincode must be 6 digits', regex='^\\d{6}$')])),
                ('owner_name', models.CharField(help_text='Full name of business owner', max_length=200)),
                ('aadhaar_number', models.CharField(blank=True, help_text='Aadhaar number (optional initially)', max_length=12, null=True, validators=[django.core.validators.RegexValidator(message='Aadhaar must be 12 digits', regex='^\\d{12}$')])),
                ('primary_categories', models.TextField(help_text='Primary product categories (comma-separated)')),
                ('brand_name', models.CharField(blank=True, help_text='Brand name or own label', max_length=200)),
                ('bank_account_number', models.CharField(blank=True, help_text='Bank account number for payouts', max_length=20, null=True)),
                ('ifsc_code', models.CharField(blank=True, help_text='IFSC code for bank transfers', max_length=11, null=True, validators=[django.core.validators.RegexValidator(message='Invalid IFSC code format', regex='^[A-Z]{4}0[A-Z0-9]{6}$')])),
                ('account_holder_name', models.CharField(blank=True, help_text='Name as per bank account', max_length=200, null=True)),
                ('upi_id', models.CharField(blank=True, help_text='UPI ID for payments', max_length=100, null=True, validators=[django.core.validators.RegexValidator(message='Invalid UPI ID format', regex='^[\\w\\.-]+@[\\w\\.-]+$')])),
                ('pan_certificate', models.FileField(blank=True, help_text='PAN certificate upload', null=True, upload_to='documents/pan/')),
                ('gst_certificate', models.FileField(blank=True, help_text='GST certificate upload', null=True, upload_to='documents/gst/')),
                ('business_logo', models.ImageField(blank=True, help_text='Business logo for branding', null=True, upload_to='logos/')),
                ('verification_status', models.CharField(choices=[('pending', 'Pending'), ('under_review', 'Under Review'), ('verified', 'Verified'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('verification_notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(help_text='Associated user account', on_delete=django.db.models.deletion.CASCADE, related_name='shopkeeper_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Business',
                'verbose_name_plural': 'Businesses',
                'ordering': ['-created_at'],
            },
        ),
    ]
