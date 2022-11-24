from functools import reduce

from common.models import BaseModel


GENDERS = ["Male", "Female"]

REGIONS = {
    "Coast": ["Mombasa", "Kwale", "Kilifi", "Tana River", "Lamu", "Taita-Taveta"],
    "North Eastern": ["Garissa", "Wajir", "Mandera"],
    "Eastern": [
        "Marsabit",
        "Isiolo",
        "Meru",
        "Tharaka-Nithi",
        "Embu",
        "Kitui",
        "Machakos",
        "Makueni",
    ],
    "Central": ["Nyandarua", "Nyeri", "Kirinyaga", "Murang'a", "Kiambu"],
    "Rift Valley": [
        "Turkana",
        "West Pokot",
        "Samburu",
        "Trans-Nzoia",
        "Uasin Gishu",
        "Elgeyo-Marakwet",
        "Nandi",
        "Baringo",
        "Laikipia",
        "Nakuru",
        "Narok",
        "Kajiado",
        "Kericho",
        "Bomet",
        "Kakamega",
        "Vihiga",
        "Bungoma",
        "Busia",
    ],
    "Nyanza": ["Siaya", "Kisumu", "Homa Bay", "Migori", "Kisii", "Nyamira"],
    "Nairobi": ["Nairobi"],
}

COUNTIES = reduce(lambda x, y: x + y, REGIONS.values(), [])

counties_to_regions_map = {}
for region, counties in REGIONS.items():
    counties = BaseModel.preprocess_choices(counties)
    for county in counties:
        counties_to_regions_map[county[0]] = region

PRACTITIONER_TYPES = [
    "Physician",
    "Nurse",
    "Lab Technician",
    "Surgeon",
    "Pharmacist",
    "Dentist",
    "Optician",
]

VISIT_TYPES = ["Outpatient", "Inpatient", "Dental", "Optical"]
ENCOUNTER_STATUS = [
    "Planned",
    "Arrived",
    "Triaged",
    "In Progress",
    "Onleave",
    "Finished",
    "Cancelled",
]
