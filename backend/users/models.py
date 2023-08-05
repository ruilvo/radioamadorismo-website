"""
Custom user model.

https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#substituting-a-custom-user-model
"""

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model.

    It's a good practice in Django to make this when you start a new project, even if you
    don't need to add any extra fields to the user model. This way, if you need to add
    something later, you won't have to create a new user model and have loads of problems.
    """
