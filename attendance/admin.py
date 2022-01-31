from django.contrib import admin
from .models import Holiday, DateTimeOfEntering, DateTimeOfExiting

admin.site.register([Holiday,DateTimeOfEntering,DateTimeOfExiting])
