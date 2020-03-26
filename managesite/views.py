from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from django.urls import resolve
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from users.models import UserProfile, Province
from information.models import MajorInfo
from .forms import AccountEditForm,MajorEditForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import render,HttpResponse
from django.contrib.auth.models import User
import xlwt
from io import StringIO,BytesIO
# Create your views here.
@login_required
def account_state(request):
    data = User.objects.all()
    profile=UserProfile.objects.all()
    context={'data': data, 'profile' : profile}
    return render(request,'account_state.html',context)


def account_edit(request,user_id):
    info = User.objects.get(id=user_id)
    if request.method != 'POST':
        form = AccountEditForm(instance=info)
    else:
        form = AccountEditForm(instance=info, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('managesite:account_state'))
    context = {'info': info, 'form': form, user_id:'user_id'}
    return render(request, 'account_edit.html', context)

def major_info(request):
    data=MajorInfo.objects.all()
    context = {'data': data}
    return render(request, 'major_info.html', context)

def major_edit(request,major_id):
    info = MajorInfo.objects.get(id=major_id)
    if request.method != 'POST':
        form = MajorEditForm(instance=info)
    else:
        form = MajorEditForm(instance=info, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('managesite:major_info'))
    context = {'info': info, 'form': form, major_id:'major_id'}
    return render(request, 'major_edit.html', context)