# Generated by Django 5.0.4 on 2024-05-05 16:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_purchaseorder_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.vendor'),
        ),
    ]
