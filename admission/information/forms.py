from django import forms
from .models import StuInfo


class StuInfoForms(forms.ModelForm):
    class Meta:
        model=StuInfo
        fields=['name','testnum','score','rank','tele','high_school','sciorart','major1','major2','major3','application_rank']
        labels={'name':'姓名','testnum':'考号','score':'分数','rank':'排名','tele':'电话','high_school':'毕业中学','sciorart':'文科/理科','major1':'第一意向专业','major2':'第二意向专业（选填）','major3':'第三意向专业（选填）','application_rank':'第几志愿'}


class SearchForms(forms.ModelForm):
    class Meta:
        model = StuInfo
        fields = ['name', 'testnum']
        labels = {'name': '姓名', 'testnum': '考号'}

class AdminEditForms(forms.ModelForm):
    class Meta:
        model=StuInfo
        fields=['name','testnum','score','rank','tele','high_school','sciorart','major1','major2','major3','is_international','application_rank','place','tip']
        labels={'name':'姓名','testnum':'考号','score':'分数','rank':'排名','tele':'电话','high_school':'毕业中学','sciorart':'文科/理科','major1':'第一意向专业','major2':'第二意向专业','major3':'第三意向专业','is_international':'是否报考国际学院','application_rank':'第几志愿','place':'地点','tip':'备注'}
        widgets = {'tip': forms.Textarea(attrs={'cols': 80})}