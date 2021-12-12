# Generated by Django 4.0 on 2021-12-12 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tenure',
            options={'ordering': ['-start']},
        ),
        migrations.AlterUniqueTogether(
            name='tenure',
            unique_together={('health_worker', 'facility', 'start')},
        ),
    ]