from django import forms
from .models import ConsultMaterial

class FileNameEdit(forms.ModelForm):
    class Meta:
        model = ConsultMaterial
        fields = ['name']
        labels = {'name': '文件名'}
