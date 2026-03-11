from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    joined_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.username
