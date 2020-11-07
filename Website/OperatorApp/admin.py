from django.contrib import admin

from .models import Operator, Mode

admin.site.register(Operator)
admin.site.register(Mode)