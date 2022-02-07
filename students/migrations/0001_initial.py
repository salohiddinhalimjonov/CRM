# Generated by Django 3.2.4 on 2022-02-07 07:27

from django.db import migrations, models
import students.models


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
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('duration', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('date_started', models.DateField()),
                ('number_of_groups', models.IntegerField()),
                ('cost_per_month', models.DecimalField(decimal_places=2, max_digits=12)),
                ('unit', models.TextField(choices=[("So'm", "So'm"), ('$', '$')], default="So'm")),
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
                ('has_been_student', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Penalty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('penalty_in_percent', models.FloatField()),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(default=students.models.generate_random_id, max_length=10, unique=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=students.models.image_path)),
                ('parent_phone_number', models.CharField(max_length=16)),
                ('date_of_receipt', models.DateField(auto_now_add=True)),
                ('has_paid_fee', models.BooleanField(default=False)),
                ('date_of_last_payment', models.DateField()),
                ('total_payment_per_month', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('unit1', models.TextField(choices=[("So'm", "So'm"), ('$', '$')], default="So'm")),
                ('total_loan_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('unit2', models.TextField(choices=[("So'm", "So'm"), ('$', '$')], default="So'm")),
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
