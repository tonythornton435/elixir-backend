from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from authentication.models import User
from common.models import BaseModel, Entity
from common.constants import REGIONS, COUNTIES, HEALTH_WORKER_TYPES


class HealthFacility(Entity):
    REGIONS = BaseModel.preprocess_choices(REGIONS)
    COUNTIES = BaseModel.preprocess_choices(COUNTIES)

    name = models.CharField("Name", max_length=128)
    region = models.CharField("Region", choices=REGIONS, max_length=32)
    county = models.CharField("County", choices=COUNTIES, max_length=32)
    location = models.TextField("Detailed Location")
    api_base_url = models.URLField("API Base URL")

    SERIALIZATION_FIELDS = [
        "uuid",
        "name",
        "region",
        "county",
        "location",
        "email",
        "phone_number",
        "address",
        "api_base_url",
        "date_joined",
        "is_active",
    ]

    def clean(self) -> None:
        if self.county not in REGIONS[self.region]:
            raise ValidationError(
                f"{self.county} does not belong to the {self.region} region"
            )
        return super().clean()


class HealthWorker(models.Model):
    HEALTH_WORKER_TYPES = BaseModel.preprocess_choices(HEALTH_WORKER_TYPES)

    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    type = models.CharField(
        "Health Worker Type", choices=HEALTH_WORKER_TYPES, max_length=32
    )
    employment_history = models.ManyToManyField(HealthFacility, through="Tenure")


class Tenure(models.Model):
    health_worker = models.ForeignKey(HealthWorker, on_delete=models.RESTRICT)
    facility = models.ForeignKey(HealthFacility, on_delete=models.RESTRICT)
    start = models.DateTimeField("Tenure Start", default=timezone.now)
    end = models.DateTimeField("Tenure End", null=True)
