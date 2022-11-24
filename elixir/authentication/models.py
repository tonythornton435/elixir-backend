import uuid

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError(_("An email must be provided."))

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

    def create_user(self, email, password, **kwargs):
        kwargs.setdefault("is_superuser", False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_superuser", True)
        if kwargs.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    class Gender(models.TextChoices):
        MALE = "MALE", _("Male")
        FEMALE = "FEMALE", _("Female")

    id = models.BigAutoField(_("Primary Key"), auto_created=True, primary_key=True)
    uuid = models.UUIDField(_("UUID"), unique=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(_("First Name"), max_length=32)
    last_name = models.CharField(_("Last Name"), max_length=32)
    country = CountryField(_("Country of Residence"))
    national_id = models.CharField(
        _("National ID Number"), blank=True, null=True, max_length=32, unique=True
    )
    gender = models.CharField(_("Gender"), max_length=6, choices=Gender.choices)
    date_of_birth = models.DateField(_("Date of Birth"))
    email = models.EmailField(_("Email Address"), unique=True)
    phone_number = PhoneNumberField(_("Phone Number"))
    date_joined = models.DateTimeField(_("Date Joined"), auto_now_add=True)
    is_active = models.BooleanField(_("Is Active"), default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "gender",
        "date_of_birth",
        "phone_number",
    ]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.get_full_name()

    @property
    def is_staff(self):
        return self.is_superuser

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name
