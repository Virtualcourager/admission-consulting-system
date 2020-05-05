from django import forms
from .models import UserProfile
from django.contrib.auth.models import User


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name')
        labels = {'username': '用户名', 'first_name': '姓名' }
        help_texts={'username': ' '}

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不匹配")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class PlaceInfoForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['telephone','province','place']
        labels={'telephone':'电话','province':'咨询省份','place':'咨询地点'}
