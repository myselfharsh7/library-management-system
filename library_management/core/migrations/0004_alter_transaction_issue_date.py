# Generated by Django 5.1.4 on 2024-12-11 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_transaction_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='issue_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
