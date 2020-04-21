from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from .models import ConsultMaterial
from .forms import FileNameEdit
from users.models import UserProfile, Province
import os
import time
from . import models
# Create your views here.


def upload(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        f=request.FILES.get('material')
        baseDir = os.path.dirname(os.path.abspath(__name__))
        jpgdir = os.path.join(baseDir, 'media')
        f.name=str(int(time.time()))+'.pdf'
        newname=f.name
        filename = os.path.join(jpgdir, f.name)
        try:
            cur=ConsultMaterial.objects.get(file_name=newname)
        except ConsultMaterial.DoesNotExist:
            models.ConsultMaterial.objects.create(file_name=newname,province_id=0,user=request.user,name=name,province_name='全国')
        data = ConsultMaterial.objects.get(file_name=newname)
        data.name = name
        data.user = request.user
        if request.user.is_superuser is True:
            data.province_id = 0
            data.province_name = '全国'
        else:
            data.province_id = UserProfile.objects.get(user=request.user).province.id
            data.province_name = UserProfile.objects.get(user=request.user).province.province
        data.save()
        fobj = open(filename, 'wb')
        for chrunk in f.chunks():
            fobj.write(chrunk)
        fobj.close()
        return HttpResponseRedirect(reverse('material:file_display'))

    else:
        return render(request, 'material/upload.html')

def admin_file_display(request):
    user_province_id = UserProfile.objects.get(user=request.user).province.id
    file = ConsultMaterial.objects.filter(province_id__in=[user_province_id, 0])
    context = {'file': file}
    return render(request, 'material/admin_file_display.html', context)

def file_display(request):
    if request.user.is_staff is True or request.user.is_superuser is True:
        return admin_file_display(request)
    user_province_id = UserProfile.objects.get(user=request.user).province.id
    file = ConsultMaterial.objects.filter(province_id__in=[user_province_id,0])
    context = {'file': file}
    return render(request, 'material/file_display.html', context)

def file_summary(request):
    if request.user.is_superuser is True:
        data=ConsultMaterial.objects.filter()
        province='全部'
    elif request.user.is_staff is True:
        user_province_id = UserProfile.objects.get(user=request.user).province.id
        data=ConsultMaterial.objects.filter(province_id=user_province_id)
        province=Province.objects.get(id=user_province_id).province
    else:
        raise Http404

    context={'data': data,'province':province}
    return render(request,'material/file_summary.html',context)

def file_editname(request,id):
    try:
        info=ConsultMaterial.objects.get(id=id)
    except ConsultMaterial.DoesNotExist:
        raise Http404
    if request.method != 'POST':
        form = FileNameEdit(instance=info)
    else:
        form = FileNameEdit(instance=info, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('material:file_summary'))

    context = {'info': info, 'form': form}
    return render(request, 'material/file_editname.html', context)

def file_delete(request,id):
    data = ConsultMaterial.objects.get(id=id)
    baseDir = os.path.dirname(os.path.abspath(__name__))
    jpgdir = os.path.join(baseDir, 'media')
    name = data.file_name
    filename = os.path.join(jpgdir, name)
    os.remove(filename)
    data.delete()
    return HttpResponseRedirect(reverse('material:file_summary'))
