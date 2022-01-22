# Generated by Django 4.0.1 on 2022-01-22 10:10

from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsentRequest',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('visit_types', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('OUTPATIENT', 'Outpatient'), ('INPATIENT', 'Inpatient'), ('OPTICAL', 'Optical'), ('DENTAL', 'Dental')], max_length=16), size=None)),
                ('request_note', models.TextField()),
                ('status', models.TextField(choices=[('DRAFT', 'Draft'), ('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('WITHDRAWN', 'Withdrawn')], max_length=16)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+254712345678'.", regex='^\\+254\\d{9}$')])),
                ('address', models.TextField()),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=128)),
                ('county', models.CharField(choices=[('MOMBASA', 'Mombasa'), ('KWALE', 'Kwale'), ('KILIFI', 'Kilifi'), ('TANA_RIVER', 'Tana River'), ('LAMU', 'Lamu'), ('TAITA_TAVETA', 'Taita-Taveta'), ('GARISSA', 'Garissa'), ('WAJIR', 'Wajir'), ('MANDERA', 'Mandera'), ('MARSABIT', 'Marsabit'), ('ISIOLO', 'Isiolo'), ('MERU', 'Meru'), ('THARAKA_NITHI', 'Tharaka-Nithi'), ('EMBU', 'Embu'), ('KITUI', 'Kitui'), ('MACHAKOS', 'Machakos'), ('MAKUENI', 'Makueni'), ('NYANDARUA', 'Nyandarua'), ('NYERI', 'Nyeri'), ('KIRINYAGA', 'Kirinyaga'), ('MURANGA', "Murang'a"), ('KIAMBU', 'Kiambu'), ('TURKANA', 'Turkana'), ('WEST_POKOT', 'West Pokot'), ('SAMBURU', 'Samburu'), ('TRANS_NZOIA', 'Trans-Nzoia'), ('UASIN_GISHU', 'Uasin Gishu'), ('ELGEYO_MARAKWET', 'Elgeyo-Marakwet'), ('NANDI', 'Nandi'), ('BARINGO', 'Baringo'), ('LAIKIPIA', 'Laikipia'), ('NAKURU', 'Nakuru'), ('NAROK', 'Narok'), ('KAJIADO', 'Kajiado'), ('KERICHO', 'Kericho'), ('BOMET', 'Bomet'), ('KAKAMEGA', 'Kakamega'), ('VIHIGA', 'Vihiga'), ('BUNGOMA', 'Bungoma'), ('BUSIA', 'Busia'), ('SIAYA', 'Siaya'), ('KISUMU', 'Kisumu'), ('HOMA_BAY', 'Homa Bay'), ('MIGORI', 'Migori'), ('KISII', 'Kisii'), ('NYAMIRA', 'Nyamira'), ('NAIROBI', 'Nairobi')], max_length=32)),
                ('location', models.TextField()),
                ('type', models.CharField(choices=[('HOSP', 'Hospital'), ('PSY', 'Psychiatry Clinic'), ('RH', 'Rehabilitation Hospital'), ('MBL', 'Medical Laboratory'), ('PHARM', 'Pharmacy'), ('PEDC', 'Pediatrics Clinic'), ('OPTC', 'Optometry Clinic'), ('DENT', 'Dental Clinic')], max_length=32)),
                ('api_base_url', models.URLField(verbose_name='API Base URL')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Practitioner',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('type', models.CharField(choices=[('PHYSICIAN', 'Physician'), ('NURSE', 'Nurse'), ('LAB_TECHNICIAN', 'Lab Technician'), ('SURGEON', 'Surgeon'), ('PHARMACIST', 'Pharmacist'), ('DENTIST', 'Dentist'), ('OPTICIAN', 'Optician')], max_length=32)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('creation_time', models.DateTimeField()),
                ('is_released', models.BooleanField(default=True)),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='records', to='registry.facility')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='records', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tenure',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('start', models.DateField(default=django.utils.timezone.now)),
                ('end', models.DateField(null=True)),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='registry.facility')),
                ('practitioner', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='employment_history', to='registry.practitioner')),
            ],
            options={
                'ordering': ['-start'],
                'unique_together': {('practitioner', 'facility', 'start')},
            },
        ),
        migrations.CreateModel(
            name='RecordRating',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('encounter', models.UUIDField()),
                ('is_accurate', models.BooleanField()),
                ('is_complete', models.BooleanField()),
                ('review', models.TextField()),
                ('rater', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='ratings', to=settings.AUTH_USER_MODEL)),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='ratings', to='registry.record')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ConsentRequestTransition',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('from_state', models.TextField(choices=[('DRAFT', 'Draft'), ('PENDING', 'Pending'), ('APPROVED', 'Approved')], max_length=16)),
                ('to_state', models.TextField(choices=[('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('WITHDRAWN', 'Withdrawn')], max_length=16)),
                ('transition_time', models.DateTimeField(auto_now_add=True)),
                ('consent_request', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='transition_logs', to='registry.consentrequest')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='consentrequest',
            name='practitioner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='registry.tenure'),
        ),
        migrations.AddField(
            model_name='consentrequest',
            name='records',
            field=models.ManyToManyField(related_name='consent_requests', to='registry.Record'),
        ),
        migrations.CreateModel(
            name='AccessLog',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('access_time', models.DateTimeField()),
                ('practitioner', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='registry.tenure')),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='access_logs', to='registry.record')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
