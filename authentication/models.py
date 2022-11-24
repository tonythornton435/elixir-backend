from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

from common.models import BaseModel, Entity
from common.constants import GENDERS


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, Entity, PermissionsMixin):
    GENDERS = BaseModel.preprocess_choices(GENDERS)

    first_name = models.CharField("First Name", max_length=32)
    surname = models.CharField("Last Name", max_length=32)
    national_id = models.CharField(
        "National ID Number", blank=True, null=True, max_length=32, unique=True
    )
    gender = models.CharField("Gender", choices=GENDERS, max_length=6)
    date_of_birth = models.DateField("Date of Birth")
    relatives = models.ManyToManyField(
        "self",
        through="NextOfKin",
        through_fields=("user", "next_of_kin"),
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "surname",
        "national_id",
        "gender",
        "date_of_birth",
        "phone_number",
    ]

    POST_REQUIRED_FIELDS = [USERNAME_FIELD, "password"] + REQUIRED_FIELDS
    SERIALIZATION_FIELDS = (
        ["uuid", USERNAME_FIELD]
        + REQUIRED_FIELDS
        + ["records", "relatives", "date_joined", "is_active"]
    )

    class Meta:
        ordering = ["-date_joined"]

    @classmethod
    def create(cls, fields):
        return User.objects.create_user(**fields)

    def __str__(self) -> str:
        return f"{self.first_name} {self.surname} ({self.uuid})"


class NextOfKin(models.Model):
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    next_of_kin = models.ForeignKey(
        User, related_name="next_of_kin", on_delete=models.CASCADE
    )
    relationship = models.CharField(
        "User's relationship to next of kin",
        choices=[
            ("SPOUSE", "Spouse"),
            ("CHILD", "Child"),
            ("PARENT", "Parent"),
            ("SIBLING", "Sibling"),
            ("OTHER_RELATIVE", "Other Relative"),
        ],
        max_length=16,
    )
    can_consent = models.BooleanField("Can consent on user's behalf?", default=False)

    POST_REQUIRED_FIELDS = ["user_id", "next_of_kin_id", "relationship", "can_consent"]
    SERIALIZATION_FIELDS = POST_REQUIRED_FIELDS
