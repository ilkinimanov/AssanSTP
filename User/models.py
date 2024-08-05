from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager (BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("User must have email")

        if not first_name:
            raise ValueError("User must have first name")

        if not last_name:
            raise ValueError("User must have last name")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        user.is_staff       = True
        user.is_admin       = True
        user.is_superuser   = True

        user.save(using=self._db)

        return user

class User (AbstractBaseUser):
    email           = models.EmailField(unique=True)
    first_name      = models.CharField(max_length=15)
    last_name       = models.CharField(max_length=15)

    is_staff        = models.BooleanField(default=False)
    is_admin        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)

    is_active       = models.BooleanField(default=True)

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
