# Generated by Django 3.2.4 on 2022-02-04 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_id',
            field=models.CharField(default='TY2E9tJPmI', max_length=10, unique=True),
        ),
    ]