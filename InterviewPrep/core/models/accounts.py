from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class UserAccountBase(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email),**kwargs)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Email is required')
       
        user = self.create_user(email, password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)   
        return user     


class UserAccount(AbstractBaseUser):
    user_id =  models.UUIDField(editable=False, unique=True, primary_key=True, default=uuid.uuid4)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = UserAccountBase()


    USERNAME_FIELD = 'email'
    
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return True