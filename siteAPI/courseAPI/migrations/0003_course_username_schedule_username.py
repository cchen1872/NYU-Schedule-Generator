# Generated by Django 4.1.7 on 2023-03-13 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseAPI', '0002_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='username',
            field=models.CharField(default='guest', max_length=20),
        ),
        migrations.AddField(
            model_name='schedule',
            name='username',
            field=models.CharField(default='guest', max_length=20),
            preserve_default=False,
        ),
    ]
