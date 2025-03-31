from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    """Custom user model.

        Extends the AbstractUser model by adding a unique email field and customizing group and permission relations.
        """
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",
        blank=True,
    )

    def __str__(self):
        """Returns the string representation of the user.

        Returns:
            The username or email of the user.
        """
        return self.username or self.email
