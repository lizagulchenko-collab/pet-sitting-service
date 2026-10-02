from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

class Animal(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        return self.create_user(email, password, **kwargs)


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STAFF = "STAFF", "Staff"
        CLIENT = "CLIENT", "Client"

    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.IntegerField(unique=True)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    role = models.CharField(
        max_length=10, choices=Role.choices, default=Role.CLIENT
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number", "city"]

    objects = CustomUserManager()


class Staff(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="staff"
    )
    age = models.IntegerField()
    bio = models.TextField(null=True, blank=True)


class Pet(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    animal = models.ForeignKey(
        Animal, on_delete=models.CASCADE, related_name="animal"
    )
    pet_parent = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="pet_parent"
    )
    allergies = models.CharField(max_length=255, null=True, blank=True)
    training_required = models.BooleanField(default=False)
    walk_times = models.IntegerField(default=0)
    additional_info = models.TextField(null=True, blank=True)
