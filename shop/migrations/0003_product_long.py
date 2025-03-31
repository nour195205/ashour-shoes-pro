# Generated by Django 5.1.7 on 2025-03-29 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='long',
            field=models.CharField(blank=True, choices=[('short', 'Short'), ('high', 'High'), ('medium', 'Medium')], default='short', max_length=10, null=True),
        ),
    ]
