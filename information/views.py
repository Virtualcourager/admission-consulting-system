from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from django.urls import resolve
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from .models import StuInfo
from .forms import StuInfoForms,SearchForms,AdminEditForms
from users.models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import render,HttpResponse
import xlwt
from io import StringIO,BytesIO
def index(request):
    return render(request,'information/index.html')

def home(request):
    return render(request,'information/home.html')

def store_success(request):
    return render(request, 'information/store_success.html')

def store_failed(request):
    return render(request, 'information/store_failed.html')

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
        curprofile=UserProfile.objects.get(user=cur)
        new_info.province=curprofile.province
        new_info.place=curprofile.place
        if new_info.major1.id>=13 :
            new_info.is_international=True
        new_info.save()
        return HttpResponseRedirect(reverse('information:store_success'))
    else:
        return HttpResponseRedirect(reverse('information:store_failed'))

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
    info=StuInfo.objects.get(id=info_id)
    if request.method!='POST':
        form=StuInfoForms(instance=info)
    else:
        form=StuInfoForms(instance=info,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('information:store_success'))

    context = {'info':info,'form': form}
    return render(request, 'information/edit_info.html', context)

@login_required
def admin_display(request):
    data = StuInfo.objects.all()
    context={'datas': data}
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
def output(request):
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
    for info in StuInfo.objects.all():
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

@login_required
def down(request):
    return render(request,'download.html')