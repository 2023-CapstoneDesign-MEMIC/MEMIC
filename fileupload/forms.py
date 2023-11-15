from django.forms import ModelForm
from .models import FileUpload
from django import forms
from .models import UploadFileModel
class DocumentForm(forms.ModelForm):
    class Meta:
        model = UploadFileModel
        fields = ("description","files")

class FileUploadForm(ModelForm):
    class Meta:
        model = FileUpload
        fields = ['title', 'imgfile', 'content']