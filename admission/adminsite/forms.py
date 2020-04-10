from .models import HistoryInfo
from django import forms

class HistoryEditForm(forms.ModelForm):
    class Meta:
        model = HistoryInfo
        fields = ['rank']
        labels = {'rank': '历史录取排名'}