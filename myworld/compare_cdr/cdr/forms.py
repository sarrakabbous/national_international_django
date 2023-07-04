from django import forms



class UploadFileForm(forms.Form):
    excel_file1 = forms.FileField(label='Sélectionnez un fichier Excel pour TT')
    excel_file2 = forms.FileField(label='Sélectionnez un fichier Excel pour l autre Opérateur')
    widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input'})

                     
