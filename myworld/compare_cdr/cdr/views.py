from django.shortcuts import render,redirect
from django.template import loader
import pandas as pd
from .models import Operateur,Telecom
from .forms import UploadFileForm
import odf
from odf import text
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook




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
                selected_columns1 = df1[['CallingNumber', 'CalledNumber', 'CallDate', 'CallHour', 'CallMinute', 'CallSecond', 'CallDuration']]
                
                # Add '216' at the beginning of CallingNumber for Telecom
                selected_columns1['CallingNumber'] = '216' + selected_columns1['CallingNumber'].astype(str)
                
                
                # Enregistrer les données dans la table Telecom
                for _, row in selected_columns1.iterrows():
                    tt_data = Telecom(
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
                selected_columns2 = df2[['CallingNumber', 'CalledNumber', 'CallDate', 'CallHour', 'CallMinute', 'CallSecond', 'CallDuration']]
                # Enregistrer les données dans la table Operateur
                for _, row in selected_columns2.iterrows():
                    other_data = Operateur(
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

                # Store the extracted data in the session
                request.session['selected_data'] = {
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
            telecom_data = Telecom.objects.all().values()
            operateur_data = Operateur.objects.all().values()
            selected_data = telecom_data.intersection(operateur_data)
        
    context = {
        'selected_data': selected_data
    }

    return render(request, 'compare.html', context)

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('main.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))
    


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            #return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "register.html", {"form": form, "msg": msg, "success": success})
