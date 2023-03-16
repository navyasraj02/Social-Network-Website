from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _


class Post(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    # ... fields and methods ...
    location = models.CharField(max_length=100)
    groups = models.ManyToManyField(
        to='auth.Group',
        related_name='custom_user_set',  # add a related_name
        blank=True,
        verbose_name=_('groups'),
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
    )
    user_permissions = models.ManyToManyField(
        to='auth.Permission',
        related_name='custom_user_set',  # add a related_name
        blank=True,
        verbose_name=_('user permissions'),
        help_text=_('Specific permissions for this user.'),
        related_query_name='custom_user',
    )
