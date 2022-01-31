# Generated by Django 4.0.1 on 2022-01-31 16:50

from django.db import migrations, models
import students.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('date_added', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='AttendedMockLesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_attending', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('duration', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('date_started', models.DateField()),
                ('number_of_groups', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OnlyContacted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=128, null=True)),
                ('address', models.CharField(blank=True, max_length=128, null=True)),
                ('phone_number', models.CharField(max_length=16)),
                ('date_of_contacting', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(default=uuid.uuid4, max_length=100, unique=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=students.models.image_path)),
                ('parent_phone_number', models.CharField(max_length=16)),
                ('has_paid_fee', models.BooleanField(default=False)),
                ('date_of_receipt', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=128)),
                ('passport_id', models.CharField(max_length=16)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=students.models.image_path)),
                ('address', models.CharField(blank=True, max_length=128, null=True)),
                ('experience', models.IntegerField()),
                ('date_of_receipt', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TimeUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
            ],
        ),
    ]