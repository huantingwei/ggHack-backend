# Generated by Django 3.0.6 on 2020-06-21 07:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_user_isprovider'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='isProvider',
        ),
        migrations.AlterField(
            model_name='service',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ownedServices', to=settings.AUTH_USER_MODEL),
        ),
    ]
