# Generated by Django 2.2.28 on 2022-07-13 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20220711_0420'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehicleinfo',
            old_name='profile',
            new_name='driver',
        ),
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], default='Monday', max_length=25, verbose_name='Day')),
                ('whole_day', models.BooleanField(default=False)),
                ('start_time', models.TimeField(default=None, null=True)),
                ('end_time', models.TimeField(default=None, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availability', to='users.DriverProfile')),
            ],
        ),
    ]