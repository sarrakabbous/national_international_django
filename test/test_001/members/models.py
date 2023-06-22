from django.db import models
from django import forms



class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  phone = models.IntegerField(null=True)
  joined_date = models.DateField(null=True)

  def __str__(self):
    return f"{self.firstname} {self.lastname}"
  
class ExcelUploadForm(forms.Form):
       excel_file = forms.FileField()


class UploadFileForm(forms.Form):
    excel_file = forms.FileField(label='Sélectionnez un fichier Excel')


# Create your models here.
