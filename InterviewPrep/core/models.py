from django.db import models
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
# from phone_field import PhoneField

# Create your models here.

class UserAccountBase(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        user = self.model(
            email = self.normalize_email(email),
        )
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)   
        return user     


class UserAccount(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    
    objects = UserAccountBase()
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return True
    

class VerificationToken(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=20)
    time_generated = models.DateTimeField()

    def __str__(self):
        return f"{self.email}: {self.otp}"


class PasswordVerificationToken(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=20)
    time_generated = models.DateTimeField()

    def __str__(self):
        return f"{self.email}: {self.otp}"