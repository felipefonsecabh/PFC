from django.contrib import admin
from .models import DataDisplay, Registers

# Register your models here.

class DisplayAdmin(admin.ModelAdmin):
    list_display=['name', 'UE', 'description']
    search_fields = ['name', 'UE']

class RegisterAdmin(admin.ModelAdmin):
    list_display=['TimeStamp', 'Temp1', 'Temp2', 'Temp3', 'Temp4', 'HotFlow', 'ColdFlow', 'PumpStatus', 'HeaterStatus', 'PumpSpeed']
    search_fields = ['TimeStamp']

admin.site.register(DataDisplay,DisplayAdmin)
admin.site.register(Registers,RegisterAdmin)
