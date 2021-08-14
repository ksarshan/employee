from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# Extending Django auth User

class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=255, blank=False, null=False,
                              error_messages={'unique': "This email has already been registered."})
    contact = models.CharField(max_length=255, blank=True, null=True)

    @property
    def full_name(self):
        return '%s %s (%s)' % (self.first_name, self.last_name, self.username)

    @property
    def show_name(self):
        return '%s %s' % (self.first_name, self.last_name)


class Employee(models.Model):
    emp_code = models.CharField(max_length=100, unique=True)
    emp_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    age = models.IntegerField()
    experience = models.IntegerField()
    objects = models.manager
    @property
    def show_desc(self):
        return '%s %s %s' % (self.emp_code, self.emp_name, self.experience)


class CSVFile(models.Model):
    file = models.FileField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = models.manager
