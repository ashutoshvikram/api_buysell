# Generated by Django 3.0.2 on 2020-04-13 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20200410_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Price',
            field=models.DecimalField(decimal_places=0, max_digits=9),
        ),
    ]