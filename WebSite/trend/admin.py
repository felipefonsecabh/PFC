from django.contrib import admin
from .models import TrendRegister

# Register your models here.

class TrendRegisterAdmin(admin.ModelAdmin):
    list_display=['TimeStamp', 'Temp1', 'Temp2', 'Temp3', 'Temp4', 'HotFlow', 'ColdFlow','PumpSpeed']
    search_fields = ['TimeStamp']

admin.site.register(TrendRegister,TrendRegisterAdmin)