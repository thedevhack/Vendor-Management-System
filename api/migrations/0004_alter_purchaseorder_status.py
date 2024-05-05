# Generated by Django 5.0.4 on 2024-05-02 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_purchaseorder_po_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='status',
            field=models.CharField(choices=[('Pending', 'pending'), ('Completed', 'completed'), ('Cancelled', 'Cancelled')], default='pending', max_length=30),
        ),
    ]
