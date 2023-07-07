from django.db import models

# Create your models here.


from django.db import models
from django import forms


class UploadFileForm(forms.Form):
    excel_file = forms.FileField(label='Sélectionnez un fichier Excel')



class Telecom(models.Model):
    CallingNumber = models.CharField(max_length=50)
    CalledNumber = models.CharField(max_length=50)
    CallDate = models.CharField(max_length=150)
    CallHour = models.IntegerField(null=True)
    CallMinute = models.IntegerField(null=True)
    CallSecond = models.IntegerField()
    CallDuration = models.IntegerField()

class Operateur(models.Model):
    CallingNumber = models.CharField(max_length=50)
    CalledNumber = models.CharField(max_length=50)
    CallDate = models.CharField(max_length=150)
    CallHour = models.IntegerField(null=True)
    CallMinute = models.IntegerField(null=True)
    CallSecond = models.IntegerField()
    CallDuration = models.IntegerField()
