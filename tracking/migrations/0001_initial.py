# Generated by Django 2.2.28 on 2022-07-14 22:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0007_auto_20220713_1849'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tracking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_at', models.DateTimeField(auto_now=True)),
                ('ended_at', models.DateTimeField(null=True)),
                ('longitude', models.CharField(max_length=50)),
                ('latitude', models.CharField(max_length=50)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.CustomerProfile')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.DriverProfile')),
            ],
        ),
    ]