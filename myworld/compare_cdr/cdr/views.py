from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
import pandas as pd
from .models import Operateur,Telecom
from .forms import UploadFileForm
import odf
from odf import text


# Create your views here.


def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

def extract_columns(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if 'compare_submit' in request.POST:
                excel_file1 = request.FILES['excel_file1']
                excel_file2 = request.FILES['excel_file2']

                # Lire les fichiers Excel
                df1 = pd.read_excel(excel_file1)
                df2 = pd.read_excel(excel_file2)

                print("Données du fichier Excel 1:")
                print(df1)
                print("Données du fichier Excel 2:")
                print(df2)

                # Extraire les colonnes désirées pour Telecom
                selected_columns1 = df1[['InSwitch', 'CallingNumber', 'CalledNumber', 'CallDate', 'CallHour', 'CallMinute', 'CallSecond', 'CallDuration']]
                # Enregistrer les données dans la table Telecom
                for _, row in selected_columns1.iterrows():
                    tt_data = Telecom(
                        InSwitch=row['InSwitch'],
                        CallingNumber=row['CallingNumber'],
                        CalledNumber=row['CalledNumber'],
                        CallDate=row['CallDate'],
                        CallHour=row['CallHour'],
                        CallMinute=row['CallMinute'],
                        CallSecond=row['CallSecond'],
                        CallDuration=row['CallDuration']
                    )
                    tt_data.save()

                # Extraire les colonnes désirées pour Operateur
                selected_columns2 = df2[['InSwitch', 'CallingNumber', 'CalledNumber', 'CallDate', 'CallHour', 'CallMinute', 'CallSecond', 'CallDuration']]
                # Enregistrer les données dans la table Operateur
                for _, row in selected_columns2.iterrows():
                    other_data = Operateur(
                        InSwitch=row['InSwitch'],
                        CallingNumber=row['CallingNumber'],
                        CalledNumber=row['CalledNumber'],
                        CallDate=row['CallDate'],
                        CallHour=row['CallHour'],
                        CallMinute=row['CallMinute'],
                        CallSecond=row['CallSecond'],
                        CallDuration=row['CallDuration']
                    )
                    other_data.save()

                # Effectuer la comparaison des données
                identical_data = [list(row.values()) for row in Telecom.objects.values()]
                tt_only_data = [list(row.values()) for row in Telecom.objects.values()]
                other_only_data = [list(row.values()) for row in Operateur.objects.values()]


                # Comparer les données et extraire les enregistrements identiques
                for _, row1 in selected_columns1.iterrows():            
                  for _, row2 in selected_columns2.iterrows():                      
                    if row1.equals(row2):
                      identical_data.append(row1.values.tolist())

                print("Données identiques:")
                print(identical_data)


                # Extraire les enregistrements uniquement de TT (Telecom)
                for _, row1 in selected_columns1.iterrows():
                  is_unique = True
                  for _, row2 in selected_columns2.iterrows():
                   if row1.equals(row2):
                     is_unique = False
                     break
                  if is_unique:
                     tt_only_data.append(row1.values.tolist())

                print("Données de TT seulement:")
                print(tt_only_data)

                # Extraire les enregistrements uniquement de l'autre opérateur
                for _, row2 in selected_columns2.iterrows():
                    is_unique = True
                    for _, row1 in selected_columns1.iterrows():
                      if row2.equals(row1):
                       is_unique = False
                       break
                if is_unique:
                   other_only_data.append(row2.values.tolist())

                print("Données de l operateur seulement:")
                print(other_only_data)

                # Passer les données au contexte
                context = {
                    'identical_data': identical_data,
                    'tt_only_data': tt_only_data,
                    'other_only_data': other_only_data,
                }
                

                # Récupérer l'option sélectionnée du combo box
                selected_option = request.POST.get('selected_option')

                # Récupérer les données depuis la base de données
                identical_data_from_db = Telecom.objects.values()
                tt_only_data_from_db = Telecom.objects.values()
                other_only_data_from_db = Operateur.objects.values()

                # Ajouter les données récupérées au contexte
                context['identical_data'] = identical_data_from_db
                context['tt_only_data'] = tt_only_data_from_db
                context['other_only_data'] = other_only_data_from_db

                return render(request, 'compare.html', {
                   
                    'column_names': selected_columns1.columns.tolist(),  # Noms des colonnes
                    'identical_data': identical_data_from_db,
                    'tt_only_data': tt_only_data_from_db,
                    'other_only_data': other_only_data_from_db,
                    'selected_option': selected_option
                    })

    else:
      form = UploadFileForm()

    return render(request, 'form.html', {'form': form})




def compare(request):
    selected_data = []
    if request.method == 'POST':
        selected_option = request.POST.get('data_select')
        if selected_option == 'telecom':
            selected_data = Telecom.objects.all()
        elif selected_option == 'operateur':
            selected_data = Operateur.objects.all()
        elif selected_option == 'both':
            selected_data = list(Telecom.objects.all()) + list(Operateur.objects.all())

    context = {
        'selected_data': selected_data
    }

    return render(request, 'compare.html', context)


  