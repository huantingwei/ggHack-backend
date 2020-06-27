# Generated by Django 3.0.6 on 2020-06-27 13:50

from django.conf import settings
import django.contrib.auth.models
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('introduction', models.TextField()),
                ('type', models.CharField(choices=[('CL', 'Clinic'), ('HS', 'Hair Salon'), ('RE', 'Restaurant'), ('SH', 'Shop')], default='SH', max_length=2)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('rating', models.FloatField()),
                ('image', models.URLField()),
                ('maxCapacity', models.IntegerField(default=10)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startTime', models.DateTimeField()),
                ('endTime', models.DateTimeField()),
                ('status', models.CharField(choices=[('CP', 'completed'), ('PD', 'pending'), ('MS', 'missed')], default='PD', max_length=2)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserved_by', to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='of_service', to='backend.Service')),
                ('serviceOwner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='of_service_owned_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CapacityTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mon', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('tue', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('wed', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('thu', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('fri', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('sat', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('sun', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Service')),
            ],
        ),
    ]
