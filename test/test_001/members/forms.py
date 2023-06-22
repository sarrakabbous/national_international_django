from django import forms



class UploadFileForm(forms.Form):
    excel_file = forms.FileField(label='Sélectionnez un fichier Excel')
    widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input'})
                     
