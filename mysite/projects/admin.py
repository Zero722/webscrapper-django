from django.contrib import admin
from .models import Employee, Configuration

# Register your models here.

admin.site.register(Employee)

class ConfigAdmin(admin.ModelAdmin):
    list_display = ('scheme_name','is_parent','parent_field', 'field','xpath', 'created', 'updated')

admin.site.register(Configuration,ConfigAdmin)

