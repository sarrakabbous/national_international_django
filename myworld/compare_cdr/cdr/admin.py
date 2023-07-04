from django.contrib import admin
from .models import Telecom, Operateur
# Register your models here.



class TelecomAdmin(admin.ModelAdmin):
    list_display = ("InSwitch", "CallingNumber", "CalledNumber", "CallDate", "CallHour", "CallMinute", "CallSecond", "CallDuration")

class OperateurAdmin(admin.ModelAdmin):
    list_display = ("InSwitch", "CallingNumber", "CalledNumber", "CallDate", "CallHour", "CallMinute", "CallSecond", "CallDuration")

admin.site.register(Telecom, TelecomAdmin)
admin.site.register(Operateur, OperateurAdmin)