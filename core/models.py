from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        RECEPTIONIST = 'RECEP', 'Receptionist'
        TECHNOLOGIST = 'TECH', 'Lab Technologist'
        PATHOLOGIST = 'PATH', 'Pathologist'
        DOCTOR = 'DOC', 'Referring Doctor'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.RECEPTIONIST)
    phone = models.CharField(max_length=20, blank=True)
    license_number = models.CharField(max_length=50, blank=True)

    def is_lab_staff(self):
        return self.role in [self.Role.TECH, self.Role.PATH, self.Role.ADMIN]
