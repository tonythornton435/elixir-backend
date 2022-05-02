# Generated by Django 4.0.3 on 2022-04-24 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='hcpcs',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='hcpcs',
            name='status_code',
            field=models.CharField(default='A', max_length=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='observation',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='observation',
            name='quantity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='observation',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='visit',
            name='discharge_disposition',
            field=models.CharField(choices=[('HOME', 'Home'), ('HOSPICE_ALTERNATIVE_HOME', 'Hospice Alternative Home'), ('HOSPICE_HEALTHCARE_FACILITY', 'Hospice HealthCare Facility'), ('ACUTE_CARE_FACILITY', 'Acute Care Facility'), ('OTHER_HEALTH_FACILITY', 'Other Health Facility'), ('EXPIRED', 'Expired'), ('LEFT_AGAINST_MEDICAL_ADVICE', 'Left Against Medical Advice'), ('NOT_DOCUMENTED', 'Not Documented')], default='NOT_DOCUMENTED', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='visit',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Draft'), ('FINALIZED', 'Finalized')], default='FINALIZED', max_length=16),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='encounter',
            name='status',
            field=models.CharField(choices=[('PLANNED', 'Planned'), ('ARRIVED', 'Arrived'), ('TRIAGED', 'Triaged'), ('IN_PROGRESS', 'In Progress'), ('ONLEAVE', 'Onleave'), ('FINISHED', 'Finished'), ('CANCELLED', 'Cancelled'), ('ENTERED_IN_ERROR', 'Entered in Error')], max_length=16),
        ),
        migrations.AlterUniqueTogether(
            name='hcpcs',
            unique_together={('code', 'description', 'status_code')},
        ),
        migrations.RemoveField(
            model_name='hcpcs',
            name='seq_num',
        ),
    ]