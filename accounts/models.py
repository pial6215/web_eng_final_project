from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    IS_STUDENT = 'student'
    IS_OWNER = 'owner'
    IS_ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (IS_STUDENT, 'Student'),
        (IS_OWNER, 'House Owner'),
        (IS_ADMIN, 'Admin'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=IS_STUDENT)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    university_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"