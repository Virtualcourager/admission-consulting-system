from django import forms
from .models import StuInfo


class StuInfoForms(forms.ModelForm):
    class Meta:
        model=StuInfo
        fields=['name','testnum','score','rank','tele','high_school','sciorart','major','application_rank']
        labels={'name':'姓名','testnum':'考号','score':'分数','rank':'排名','tele':'电话','high_school':'毕业中学','sciorart':'文科/理科','major':'意向专业','application_rank':'第几志愿'}


class SearchForms(forms.ModelForm):
    class Meta:
        model = StuInfo
        fields = ['name', 'testnum']
        labels = {'name': '姓名', 'testnum': '考号'}

class AdminEditForms(forms.ModelForm):
    class Meta:
        model=StuInfo
        fields=['name','testnum','score','rank','tele','high_school','sciorart','major','application_rank','staff_id','place','tip']
        labels={'name':'姓名','testnum':'考号','score':'分数','rank':'排名','tele':'电话','high_school':'毕业中学','sciorart':'文科/理科','major':'意向专业','application_rank':'第几志愿','staff_id':'录入人员','place':'地点','tip':'备注'}
        widgets = {'tip': forms.Textarea(attrs={'cols': 80})}