# Generated by Django 2.2.28 on 2022-07-04 17:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.utils


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20220702_1405'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customerprofile',
            options={'ordering': ['-id'], 'verbose_name': 'Customer Profile', 'verbose_name_plural': 'Customer Profiles'},
        ),
        migrations.RemoveField(
            model_name='customerprofile',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='customerprofile',
            name='status',
        ),
        migrations.AddField(
            model_name='customerprofile',
            name='country',
            field=models.CharField(choices=[('us', 'US')], default='us', max_length=10, verbose_name='Country'),
        ),
        migrations.AddField(
            model_name='customerprofile',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='customerprofile',
            name='is_female',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='customerprofile',
            name='is_verify_mail_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='document_back_photo',
            field=models.ImageField(upload_to=users.utils.file_upload, validators=[users.utils.file_validation]),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='document_front_photo',
            field=models.ImageField(upload_to=users.utils.file_upload, validators=[users.utils.file_validation]),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='face_photo',
            field=models.ImageField(upload_to=users.utils.file_upload, validators=[users.utils.file_validation]),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='profile_image',
            field=models.ImageField(upload_to=users.utils.file_upload, validators=[users.utils.file_validation]),
        ),
        migrations.CreateModel(
            name='VerificationCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=6)),
                ('is_used', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='verification_code', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DriverProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, verbose_name='Full name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('date_of_birth', models.DateField(verbose_name='Date of birth')),
                ('phone', models.CharField(max_length=100, verbose_name=' Phone')),
                ('is_female', models.BooleanField(default=True)),
                ('address', models.TextField(verbose_name='Address')),
                ('city', models.CharField(max_length=100, verbose_name='City')),
                ('zip_code', models.CharField(max_length=100, verbose_name='Zip code')),
                ('state', models.CharField(max_length=100, verbose_name='State')),
                ('country', models.CharField(choices=[('us', 'US')], default='us', max_length=10, verbose_name='Country')),
                ('identity_document_no', models.CharField(max_length=100, verbose_name='Identity document number')),
                ('profile_image', models.ImageField(upload_to=users.utils.file_upload, validators=[users.utils.file_validation])),
                ('is_verify', models.BooleanField(default=False)),
                ('is_verify_mail_sent', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='driver_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Driver Profile',
                'verbose_name_plural': 'Driver Profiles',
                'ordering': ['-id'],
            },
        ),
    ]
