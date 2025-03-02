from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.crypto import get_random_string

class UserManager(BaseUserManager):
    def create_user(self, email, full_name, address, phone, partner_type, sponsor, branch, password=None):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, address=address, phone=phone, partner_type=partner_type, sponsor=sponsor, branch=branch)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password):
        user = self.create_user(email=email, full_name=full_name, address='', phone='', partner_type='admin', sponsor=None, branch='', password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    PARTNER_TYPES = [
        ('standard', 'Стандартный партнер'),
        ('vip', 'VIP партнер'),
        ('admin', 'Администратор'),
    ]

    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    partner_type = models.CharField(max_length=20, choices=PARTNER_TYPES, default='standard')
    sponsor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    branch = models.CharField(max_length=10, blank=True, null=True)
    referral_link_1 = models.CharField(max_length=50, unique=True, blank=True, null=True)
    referral_link_2 = models.CharField(max_length=50, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def save(self, *args, **kwargs):
        if not self.referral_link_1:
            self.referral_link_1 = f"https://s1.sublar.kz/ref{get_random_string(10)}"
        if not self.referral_link_2:
            self.referral_link_2 = f"https://s1.sublar.kz/ref{get_random_string(10)}"
        super().save(*args, **kwargs)
