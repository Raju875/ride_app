from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager 
from users.utils import *

class UserType:
    ADMIN = 1
    CUSTOMER = 2
    DRIVER = 3

    Choices = (
        (ADMIN, 'ADMIN'),
        (CUSTOMER, 'CUSTOMER'),
        (DRIVER, 'DRIVER'),
    )


class COUNTRY_CHOICES:
    us = 'us'

    Choices = (
        (us, 'US'),
    )


class User(AbstractUser):
    name = models.CharField(_("Name of User"), blank=True, null=True, max_length=255)
    user_type = models.IntegerField(_('User type'), choices=UserType.Choices, default=UserType.CUSTOMER)

    objects = CustomUserManager()

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"name": self.name})


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    full_name = models.CharField(_('Full name'), max_length=100)
    email = models.EmailField(_('Email'), unique=True)
    date_of_birth = models.DateField(_('Date of birth'))
    phone = models.CharField(_(' Phone'), max_length=100)
    is_female = models.BooleanField(default=True)
    address = models.TextField(_('Address'))
    city = models.CharField(_('City'), max_length=100)
    zip_code = models.CharField(_('Zip code'), max_length=100)
    state = models.CharField(_('State'), max_length=100)
    country = models.CharField(_('Country'), choices=COUNTRY_CHOICES.Choices, default=COUNTRY_CHOICES.us,  max_length=10)
    is_approved = models.BooleanField(default=False)
    is_verify_mail_sent = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.full_name

    class Meta:
        verbose_name = _('Customer Profile')
        verbose_name_plural = _("Customer Profiles")
        ordering = ['-id']


class CustomerDocuments(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_document')
    customer = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE, related_name='customer_document', null=True)
    document_front_photo = models.ImageField(upload_to=file_upload, validators=[file_validation], null=True)
    document_back_photo = models.ImageField(upload_to=file_upload, validators=[file_validation], null=True)
    face_photo = models.ImageField(upload_to=file_upload, validators=[file_validation], null=True)
    profile_image = models.ImageField(upload_to=file_upload, validators=[file_validation], null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.user.email

    class Meta:
        verbose_name = _('Customer Document')
        verbose_name_plural = _("Customer Documents")
        ordering = ['-id']


class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    full_name = models.CharField(_('Full name'), max_length=100)
    email = models.EmailField(_('Email'), unique=True)
    phone = models.CharField(_(' Phone'), max_length=100)
    identity_document_no = models.CharField(_('Identity document number'), max_length=100)
    tax_no = models.CharField(_('Tax number'), max_length=100, null=True)
    date_of_birth = models.DateField(_('Date of birth'))
    is_female = models.BooleanField(default=True)
    address = models.TextField(_('Address'))
    city = models.CharField(_('City'), max_length=100)
    zip_code = models.CharField(_('Zip code'), max_length=100)
    state = models.CharField(_('State'), max_length=100)
    country = models.CharField(_('Country'), choices=COUNTRY_CHOICES.Choices, default=COUNTRY_CHOICES.us,  max_length=10)
    # profile_image = models.ImageField(upload_to=file_upload, validators=[file_validation])
    # address_photo = models.ImageField(upload_to=file_upload, validators=[file_validation], null=True, blank=True)
    # license_front_photo = models.ImageField(upload_to=file_upload, validators=[file_validation], null=True, blank=True)
    # license_back_photo = models.ImageField(upload_to=file_upload, validators=[file_validation], null=True, blank=True)
    # identity_document_front_photo = models.ImageField(upload_to=file_upload, validators=[file_validation], null=True, blank=True)
    # identity_document_back_photo = models.ImageField(upload_to=file_upload, validators=[file_validation], null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    is_verify_mail_sent = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.full_name

    class Meta:
        verbose_name = _('Driver Profile')
        verbose_name_plural = _("Driver Profiles")
        ordering = ['-id']


class VehicleInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vehicle_info')
    driver = models.OneToOneField(DriverProfile, on_delete=models.CASCADE, related_name='vehicle_info')
    model = models.CharField(_('Model name'), max_length=255)
    year = models.IntegerField(_('Year'))
    license_plate_nubmer = models.CharField(_('License plate number'), max_length=255)
    driver_license_number = models.CharField(_('Driving license number'), max_length=255)
    license_issued_in = models.CharField(_('License issued in'), max_length=100)
    mvr_document = models.FileField(upload_to=file_upload, validators=[file_validation])
    insurance_document = models.FileField(upload_to=file_upload, validators=[file_validation])
    operating_card_document = models.FileField(upload_to=file_upload, validators=[file_validation])
    inspection_document = models.FileField(upload_to=file_upload, validators=[file_validation])
    image = models.ImageField(upload_to=file_upload, validators=[file_validation])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.model

    class Meta:
        verbose_name = _('Vehicle Info')
        verbose_name_plural = _("Vehicle Infos")
        ordering = ['-id']


def get_verification_code():
    from random import randint
    return randint(1000, 9999)


class VerificationCode(models.Model):
    user = models.OneToOneField(User, related_name="verification_code", on_delete=models.CASCADE)
    code = models.CharField(max_length=6, db_index=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    def __str__(self):
        return str(self.code)

    @staticmethod
    def generate_code_for_user(user):
        if hasattr(user, "verification_code"):
            obj = user.verification_code
            obj.code = get_verification_code()
            obj.is_used = False
            obj.save()
        else:
            obj = VerificationCode.objects.create(
                user=user, code=get_verification_code(), is_used=False)      

        return obj.code
