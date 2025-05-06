from django.db import models
from django.contrib.auth.models import AbstractBaseUser,UserManager
from django.db.models import OneToOneField
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# Create your models here.

from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not username:
            raise ValueError('Username is required')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,username,email,password=None,**extra_fields):
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_admin',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(username=username,password=password,email=email,**extra_fields)

class User(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER = 2
    ROLE_CHOICES = (
        (VENDOR,'VENDOR'),
        (CUSTOMER,'CUSTOMER')
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=12,blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES,blank=True,null=True)
    
    # required fields
    date_joined = models.DateTimeField(auto_now_add= True)
    modified_date =  models.DateTimeField(auto_now= True)
    last_login =  models.DateTimeField(auto_now_add= True)
    created_date =  models.DateTimeField(auto_now_add= True)
    
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']
    
    objects = UserManager()
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self,app_label):
        return True
    
class UserProfile(models.Model):
    user = OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    profile_picture = models.ImageField(upload_to='users/profile_pictures',blank=True,null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos',blank=True,null=True)
    address_line1 = models.CharField(max_length=50,blank=True,null=True)
    address_line2 = models.CharField(max_length=50,blank=True,null=True)
    country = models.CharField(max_length=50,blank=True,null=True)
    state = models.CharField(max_length=50,blank=True,null=True)
    city = models.CharField(max_length=50,blank=True,null=True)
    pin_code = models.CharField(max_length=50,blank=True,null=True)
    latitude = models.CharField(max_length=50,blank=True,null=True)
    longitude = models.CharField(max_length=50,blank=True,null=True)
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.email
    
    
    

    
    
    
