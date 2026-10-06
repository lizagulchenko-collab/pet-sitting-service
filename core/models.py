from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

class Animal(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Animal type"
        verbose_name_plural = "Animal types"


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
    phone_number = models.CharField(max_length=20, unique=True)
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


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        IN_PROGRESS = "IN_PROGRESS", "In_progress"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELED", "Canceled"
        REJECTED = "REJECTED", "Rejected"

    pet = models.ForeignKey(
        Pet, on_delete=models.CASCADE, related_name="pet"
    )
    staff = models.ForeignKey(
        Staff, on_delete=models.DO_NOTHING, related_name="booking", null=True, blank=True
    )
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    total_price = models.IntegerField()
