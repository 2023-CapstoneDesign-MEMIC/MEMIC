from django.forms import ModelForm
from .models import FileUpload
from django import forms

class FileUploadForm(ModelForm):
    class Meta:
        model = FileUpload
        fields = ['audiofile', 'start', 'end']