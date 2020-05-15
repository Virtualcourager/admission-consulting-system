from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from django.urls import resolve
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from .models import StuInfo,RankPredict
from .forms import StuInfoForms,SearchForms,AdminEditForms
from users.models import UserProfile, Province
from material.models import ConsultMaterial
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import render,HttpResponse
import xlwt
from . import models

from io import StringIO,BytesIO

@login_required
def admin_index(request):
    if request.user.is_superuser is True or request.user.is_staff is True:
        return render(request, 'information/admin_index.html')
    else:
        raise Http404

@login_required
def index(request):
    if request.user.is_superuser is True or request.user.is_staff is True:
        return admin_index(request)
    else:
        user_province_id = UserProfile.objects.get(user=request.user).province.id
        file = ConsultMaterial.objects.filter(province_id__in=[user_province_id, 0])[:2]
        tele = UserProfile.objects.get(user=request.user).telephone
        print(tele)
        context = {'file': file, 'tele':tele, 'name':request.user.first_name}
        return render(request,'information/index.html', context)

def stu_menu(request):
    return render(request,'information/stu_menu.html')

def store_success(request):
    return render(request, 'information/store_success.html')

def store_failed(request):
    return render(request, 'information/store_failed.html')

def exists(request,info_id ,info_testnum):
    context = {'info_id': info_id, 'info_testnum': info_testnum}
    return render(request, 'information/exists.html',context)

def update_predict(new_info):
    try:
        data = RankPredict.objects.get(score=new_info.score,province_id=new_info.province_id,sciorart_id=new_info.sciorart_id)
        if data.highrank > new_info.rank or data.highrank is 0:
            data.highrank = new_info.rank
        if data.lowrank < new_info.rank or data.lowrank is 0:
            data.lowrank = new_info.rank
    except RankPredict.DoesNotExist:
        models.RankPredict.objects.create(score=new_info.score,province_id=new_info.province_id,sciorart_id=new_info.sciorart_id)
        data = RankPredict.objects.get(score=new_info.score, province_id=new_info.province_id,sciorart_id=new_info.sciorart_id)
        data.highrank= new_info.rank
        data.lowrank = new_info.rank
    data.save()
def dupcheck(request,form):
    data = form.cleaned_data
    curnum = data['testnum']
    curname = data['name']
    try:
        dup = StuInfo.objects.get(name=curname, testnum=curnum)
    except StuInfo.DoesNotExist:
        dup = None
    if dup is None:
        new_info=form.save(commit=False)
        cur= request.user
        new_info.staff = cur
        curprofile = UserProfile.objects.get(user=cur)
        new_info.province=curprofile.province
        new_info.place=curprofile.place
        if new_info.major1.is_international is 1:
            new_info.is_international=True
        if new_info.major2:
            if new_info.major2.is_international is 1:
                new_info.is_international=True
        if new_info.major3:
            if new_info.major3.is_international is 1:
                new_info.is_international=True
        update_predict(new_info)
        new_info.save()
        return HttpResponseRedirect(reverse('information:store_success'))
    else:
        return HttpResponseRedirect(reverse('information:exists', kwargs={"info_id":dup.id,"info_testnum":dup.testnum}))

@login_required
def new_stu(request):
    if request.method!='POST':
        form=StuInfoForms()
    else:
        form=StuInfoForms(request.POST)
        if form.is_valid():
            return dupcheck(request,form)

    context={'form':form}
    return render(request, 'information/new_stu.html', context)

@login_required
def search_info(request):
    if request.method!='POST':
        form=SearchForms()
    else:
        form=SearchForms(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            curnum = data['testnum']
            curname = data['name']
            try:
                dup = StuInfo.objects.get(name=curname, testnum=curnum)
            except StuInfo.DoesNotExist:
                dup = None
            if dup is None:
                return HttpResponseRedirect(reverse('information:store_failed'))
            else:
                return HttpResponseRedirect(reverse('information:edit_info', kwargs={"info_id":dup.id,"info_testnum":dup.testnum}))
    context={'form':form}
    return render(request, 'information/search_info.html', context)

@login_required
def edit_info(request,info_id ,info_testnum):
    try:
        info=StuInfo.objects.get(id=info_id,testnum=info_testnum)
    except StuInfo.DoesNotExist:
        raise Http404
    if request.method!='POST':
        form=StuInfoForms(instance=info)
    else:
        form=StuInfoForms(instance=info,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('information:store_success'))

    context = {'info':info,'form': form}
    return render(request, 'information/edit_info.html', context)

def admin_only(request):
    if request.user.is_staff is False:
        raise Http404

@login_required
def admin_display(request):
    admin_only(request)
    data = []
    provinces= Province.objects.all()
    curprofile = UserProfile.objects.get(user=request.user)
    default = curprofile.province
    if not default:
        default = 1
    province_id = request.GET.get('province','')
    if province_id:
        data = StuInfo.objects.filter(province=province_id)
    else:
        data = StuInfo.objects.filter(province=default)
        province_id = default.id

    context={'datas': data,'cur_province':province_id, 'provinces': provinces, 'default': default}
    return render(request,'information/admin_display.html',context)

@login_required
def admin_edit(request,info_id):
    info = StuInfo.objects.get(id=info_id)
    if request.method != 'POST':
        form = AdminEditForms(instance=info)
    else:
        form = AdminEditForms(instance=info, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('information:admin_display'))

    context = {'info': info, 'form': form}
    return render(request, 'information/admin_edit.html', context)


@login_required
def output(request,province_id):
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=information.xls'
    wb = xlwt.Workbook(encoding = 'utf-8')
    sheet = wb.add_sheet(u'考生信息')
    #1st line
    sheet.write(0,0, '编号')
    sheet.write(0,1, '姓名')
    sheet.write(0,2, '考号')
    sheet.write(0,3, '成绩')
    sheet.write(0,4, '排名')
    sheet.write(0,5, '电话')
    sheet.write(0,6, '毕业高中')
    sheet.write(0,7, '文理科')
    sheet.write(0, 8, '第一意向专业')
    sheet.write(0, 9,'第二意向专业')
    sheet.write(0, 10, '第三意向专业')
    sheet.write(0, 11, '是否填报国际学院')
    sheet.write(0, 12, '第几志愿')
    sheet.write(0, 13, '省份')
    sheet.write(0, 14, '录入教师')
    sheet.write(0, 15, '咨询点')
    sheet.write(0, 16, '备注')
    sheet.write(0, 17, '录入日期')
    sheet.write(0, 18, '录入时间')
    row=1
    for info in StuInfo.objects.filter(province=province_id):
        sheet.write(row, 0, info.id)
        sheet.write(row, 1, info.name)
        sheet.write(row, 2, info.testnum)
        sheet.write(row, 3, info.score)
        sheet.write(row, 4, info.rank)
        sheet.write(row, 5, info.tele)
        sheet.write(row, 6, info.high_school)
        sheet.write(row, 7, str(info.sciorart))
        sheet.write(row, 8, str(info.major1))
        sheet.write(row, 9, str(info.major2))
        sheet.write(row, 10, str(info.major3))
        sheet.write(row, 11, str(info.is_international))
        sheet.write(row, 12, info.application_rank)
        sheet.write(row, 13, str(info.province))
        sheet.write(row, 14, info.staff.first_name)
        sheet.write(row, 15, info.place)
        sheet.write(row, 16, info.tip)
        sheet.write(row, 17, str(info.date))
        sheet.write(row, 18, str(info.time))
        row = row + 1
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    response.write(output.getvalue())
    return response

def rank_display(request):
    admin_only(request)
    provinces= Province.objects.all()
    curprofile = UserProfile.objects.get(user=request.user)
    default = curprofile.province
    province_id = request.GET.get('province','')
    if not province_id:
        province_id=default
    datas=RankPredict.objects.filter(province=province_id)
    for data in datas:
        data.delete()
    datas=StuInfo.objects.filter(province=province_id)
    for data in datas:
        update_predict(data)
    scidata = []
    artdata = []
    if province_id:
        scidata = RankPredict.objects.filter(province=province_id,sciorart=1).order_by('-score')
        artdata = RankPredict.objects.filter(province=province_id, sciorart=2).order_by('-score')
    if len(scidata) > 0:
        cur=scidata[0].score
        for data in scidata:
            while data.score != cur:
                models.RankPredict.objects.create(score=cur,province=data.province,sciorart=data.sciorart,highrank=0,lowrank=0)
                cur=cur-1
            cur=cur-1
    if len(artdata) > 0:
        cur=artdata[0].score
        for data in artdata:
            while data.score is not cur:
                models.RankPredict.objects.create(score=cur,province=data.province,sciorart=data.sciorart,highrank=0,lowrank=0)
                cur = cur - 1
            cur = cur - 1
    scidata = RankPredict.objects.filter(province=province_id, sciorart=1).order_by('-score')
    artdata = RankPredict.objects.filter(province=province_id, sciorart=2).order_by('-score')
    context={'scidata': scidata,'artdata': artdata, 'provinces': provinces, 'default': default}
    return render(request,'information/rank_display.html',context)

def delete(request,info_id):
    data=StuInfo.objects.get(id=info_id)
    data.delete()
    return HttpResponseRedirect(reverse('information:admin_display'))