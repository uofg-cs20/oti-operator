from django.contrib import admin

from .models import Operator, Mode

class OperatorAdmin(admin.ModelAdmin):
    list_display = ('admin', 'name', 'get_modes', 'homepage', 'api_url', 'default_language', 'phone', 'email', 'active')

    def get_modes(self, obj):
        return "\n".join([mode.short_desc for mode in obj.modes.all()])

class ModeAdmin(admin.ModelAdmin):
    list_display = ('short_desc', 'long_desc')

admin.site.register(Operator, OperatorAdmin)
admin.site.register(Mode, ModeAdmin)