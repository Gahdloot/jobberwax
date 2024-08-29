from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
import uuid

from datetime import datetime, timedelta
from django.utils import timezone
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must has an email address")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class UserType(models.TextChoices):
        Agent = "Agent", _("Agent")
        Manager = "Manager", _("Manager")
        Admin = "Admin", _("Admin")
    

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(unique=True, max_length=254, null=True)
    password = models.CharField(max_length=255, null=False)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    is_blacklisted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Organisation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=150, blank=True, null=True)
    admin_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    staff_access_code = models.CharField(max_length=100, null=False)
    num_of_staffs = models.IntegerField(default=1)
    valuation = models.CharField(max_length=10, null=False)
    country = models.CharField(max_length=70, blank=True, null=True)
    state = models.CharField(max_length=70, blank=True, null=True)
    city = models.CharField(max_length=70, blank=True, null=True)
    address = models.CharField(max_length=70, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True)


class OrganisationUser(models.Model):
    class Roles(models.TextChoices):
        ORG_ADMIN = "ORG_ADMIN", _("ORG_ADMIN")
        ORG_STAFF = "ORG_STAFF", _("ORG_STAFF")
        ORG_HR = "ORG_HR", _("ORG_HR")
        UNASSIGNED = "UNASSIGNED", _("UNASSIGNED")
    organisation = models.ForeignKey(Organisation, on_delete=models.SET_NULL, null=True)
    role = models.TextField(choices=Roles.choices, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True)
