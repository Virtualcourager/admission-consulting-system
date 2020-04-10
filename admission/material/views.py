from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from .models import ConsultMaterial
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
            models.ConsultMaterial.objects.create(file_name=newname,province_id=0,user=request.user,name=name)
        data = ConsultMaterial.objects.get(file_name=newname)
        data.name = name
        data.user = request.user
        if request.user.is_superuser is True:
            data.province_id = 0
        else:
            data.province_id = UserProfile.objects.get(user=request.user).province.id
        data.save()
        fobj = open(filename, 'wb')
        for chrunk in f.chunks():
            fobj.write(chrunk)
        fobj.close()
        return HttpResponseRedirect(reverse('information:store_success'))

    else:
        return render(request, 'material/upload.html')

def file_display(request):
    user_province_id = UserProfile.objects.get(user=request.user).province.id
    file = ConsultMaterial.objects.filter(province_id__in=[user_province_id,0])
    context = {'file': file}
    return render(request, 'material/file_display.html', context)

def file_summary(request):
    if request.user.is_superuser is True:
        data=ConsultMaterial.objects.filter()
        province='全部'
    elif request.user.is_admin is True:
        user_province_id = UserProfile.objects.get(user=request.user).province.id
        data=ConsultMaterial.objects.filter(province_id=user_province_id)
        province=Province.objects.get(id=user_province_id).province
    else:
        raise Http404

    context={'data': data,'province':province}
    return render(request,'material/file_summary.html',context)
