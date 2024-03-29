from random import randint
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator, MinLengthValidator
# Create your models here.

class CustomUser(BaseUserManager):
    """
    Custom user model manager where email is the Unique identifier
    for authentication instead of username.
    """

    def _create_user(self, email, password, is_active, is_staff, is_superuser, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('Email must be provided.'))

        if not password:
            raise ValueError(_('Password must be provided.'))

        email = self.normalize_email(email)  # normalize_email is used to validate the given email.
        user = self.model(email=email, is_active=is_active, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):

        return self._create_user(email, password, is_active=True, is_staff=False, is_superuser=False, **extra_fields)

    def create_superuser(self, email, password, is_active=True, is_staff=True, is_superuser=True, **extra_fields):
        '''
        It will create a superuser with the given email and password
        '''
        user = self._create_user(email, password, is_staff=is_staff, is_active=is_active, is_superuser=is_superuser, **extra_fields)
        user.save(using=self._db)
        return user

class SuperUser(AbstractBaseUser, PermissionsMixin):
    """docstring for ClassName"""
    USER_TYPE_CHOICE = [
        ('1','Patient'),
        ('2','Doctor')
    ]
    username = models.CharField(verbose_name=_("Username"), max_length=255, blank=True, unique=True, default='')
    email = models.EmailField(_('Email Address'), unique=True) 
    first_name = models.CharField(_('First Name'), blank=True, max_length=200)
    last_name = models.CharField(_('Last Name'), blank=True, max_length=200)
    phone = models.CharField(_('Phone'), blank=True, default='', max_length=15)
    address = models.CharField(_('Address'), blank=True, max_length=300) 
    user_type = models.CharField( max_length=2, choices=USER_TYPE_CHOICE)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'address', 'user_type']

    objects = CustomUser()

    def save(self, *args, **kwargs):
        if not self.username: 
            if SuperUser.objects.filter(username=self.first_name.lower()).exists():
                extra = str(randint(1, 10000))
                self.username = slugify(self.first_name) + "-" + extra
            else:
                self.username = slugify(self.first_name) 
        super(SuperUser, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def token_creation(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)

class UserOtp(models.Model):
    otp_number = models.CharField(max_length=20, default='')
    user_email = models.EmailField(max_length=100, default='')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = 'Otps'
        verbose_name_plural = 'Otps'
            
    def __str__(self):
        return 'OTP for '+ self.user_email

class MedicalHistory(models.Model):
    user=models.ForeignKey(SuperUser, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='uploads/medical_history')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = 'Users Medical History'
        verbose_name_plural = 'Users Medical History'
    
    def __str__(self):
        return 'Medical History of '+ self.user.first_name


class Appointment(models.Model):
    user=models.ForeignKey(SuperUser, on_delete=models.CASCADE)
    appointment_day   = models.IntegerField(
        validators=[MaxValueValidator(31), MinValueValidator(1)] 
        )
    appointment_month = models.IntegerField(
        validators=[MaxValueValidator(12), MinValueValidator(1)] 
        )
    appointment_year  = models.IntegerField()
    appointment_time  = models.TimeField(blank=True, null=True) 
    description = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = 'Users Appointment'
        verbose_name_plural = 'Users Appointment'
    
    def __str__(self):
        return 'Appointment of '+ self.user.first_name
    
class Heartbeat(models.Model):
    user=models.ForeignKey(SuperUser, on_delete=models.CASCADE, blank=True)
    oxygen_level   = models.CharField(max_length=20)
    heart_rate = models.CharField(max_length=20)
    temperature  = models.CharField(max_length=20) 
    description = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = 'Users Heartbeat'
        verbose_name_plural = 'Users Heartbeat'
    
    def __str__(self):
        return 'Heartbeat of '+ self.user.first_name
    
class MedicalForm(models.Model):
    doctor = models.ForeignKey(SuperUser, on_delete=models.CASCADE, related_name='doctor_user')
    attachment = models.FileField(upload_to='uploads/medical_form')
    patient = models.ForeignKey(SuperUser, on_delete=models.DO_NOTHING, related_name='patient')
    description = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = 'Users Medical form'
        verbose_name_plural = 'Users Medical form'
    
    def __str__(self):
        return 'Medical form of '+ self.patient.first_name