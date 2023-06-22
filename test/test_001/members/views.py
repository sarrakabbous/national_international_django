import pandas as pd

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Member
from .forms import UploadFileForm




def members(request):
  mymembers = Member.objects.all().values()
  template = loader.get_template('all_members.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))

def details(request, id):
  mymember = Member.objects.get(id=id)
  template = loader.get_template('details.html')
  context = {
    'mymember': mymember,
  }
  return HttpResponse(template.render(context, request))

def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

def testing(request):
  template = loader.get_template('template.html')
  context = {
    'fruits': ['Apple', 'Banana', 'Cherry'],   
  }
  return HttpResponse(template.render(context, request))


def extract_columns(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)  # Charger le fichier Excel avec pandas
            columns = df.columns.tolist()  # Extraire les noms des colonnes
            # Faire quelque chose avec les colonnes extraites, par exemple les afficher
            return render(request, 'result.html', {'columns': columns})
    else:
        form = UploadFileForm()
    return render(request, 'form.html', {'form': form})