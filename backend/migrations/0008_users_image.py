# Generated by Django 3.0.2 on 2020-04-22 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_auto_20200420_0040'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='Image',
            field=models.ImageField(null=True, upload_to='profile'),
        ),
    ]
