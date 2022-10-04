from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractUser
)
from datetime import datetime


class UserManager(BaseUserManager):
    def create_user(self, username, email, mobile_number, password=None):
        """
        Creates and saves a User with the given username, phone, password.
        """
        if not username:
            raise ValueError('Users must have a username')
        if not mobile_number:
            raise ValueError('Users must have a mobile number')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            mobile_number=mobile_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, mobile_number, password=None):
        """
        Creates and saves a superuser with the given email, password.
        """
        user = self.create_user(
            username=username,
            email=email,
            mobile_number=mobile_number,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    mobile_number = models.CharField(max_length=10)
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.CharField(max_length=255, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_senior_citizen = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'mobile_number']

    def save(self, *args, **kwargs):
        if self.date_of_birth:
            date = datetime.now() - datetime.strptime(str(self.date_of_birth), "%Y-%m-%d")
            total_years = date.total_seconds()/(365.242*24*3600)
            # total_months = (total_years - int(total_years))*12
            # total_days = (total_months - int(total_months))*24
            self.age = f"{int(total_years)}"
        if self.age:
            if int(self.age) >= 60:
                self.is_senior_citizen = True
            else:
                self.is_senior_citizen = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
