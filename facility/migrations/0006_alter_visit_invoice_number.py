# Generated by Django 4.0.3 on 2022-05-02 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0005_chargeitem_created_chargeitem_updated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='invoice_number',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]
