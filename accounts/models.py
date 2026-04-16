from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=200, blank=True)
    avatar_initials = models.CharField(max_length=3, blank=True)
    plan = models.CharField(max_length=20, default='free', choices=[('free','Free'),('pro','Pro'),('enterprise','Enterprise')])
    email_verified = models.BooleanField(default=False)
    onboarding_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if self.full_name and not self.avatar_initials:
            parts = self.full_name.split()
            self.avatar_initials = ''.join(p[0].upper() for p in parts[:2])
        elif self.email and not self.avatar_initials:
            self.avatar_initials = self.email[0].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    @property
    def display_name(self):
        return self.full_name or self.email.split('@')[0]
