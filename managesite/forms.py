from django import forms
from django.contrib.auth.models import User
from information.models import MajorInfo

class AccountEditForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['is_active','is_staff']
        labels={'is_active':'登录权限','is_staff':'管理员权限'}
        help_texts={'is_active': ('勾选以允许用户使用此账户登陆'), 'is_staff': ('勾选以允许用户使用此账户访问/编辑/下载汇总信息')}

class MajorEditForm(forms.ModelForm):
    class Meta:
        model=MajorInfo
        fields=['major_name','sciorart','is_international']
        labels={'major_name':'专业名称','sciorar':'文理科','is_international':'是否为国院专业'}
        help_texts={'is_international': ('勾选以代表其为国际学院专业')}