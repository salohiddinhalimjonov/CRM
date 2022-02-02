# Generated by Django 3.2.4 on 2022-02-02 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('students', '0003_auto_20220202_1613'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='education_centre',
        ),
        migrations.AddField(
            model_name='course',
            name='education_centre',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.educationcentre'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='onlycontacted',
            name='education_centre',
        ),
        migrations.AddField(
            model_name='onlycontacted',
            name='education_centre',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.educationcentre'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='education_centre',
        ),
        migrations.AddField(
            model_name='teacher',
            name='education_centre',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.educationcentre'),
            preserve_default=False,
        ),
    ]
