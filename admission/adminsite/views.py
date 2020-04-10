from django.shortcuts import render
from .models import HistoryInfo,BorderlinePredict
from users.models import UserProfile, Province
from information.models import MajorInfo,RankPredict
from . import models
from .forms import HistoryEditForm
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
def admin_only(request):
    if request.user.is_staff is False:
        raise Http404

@login_required
def history_info(request):
    admin_only(request)
    province=UserProfile.objects.get(user=request.user).province
    majors=MajorInfo.objects.all()
    for major in majors:
        try:
            cur = HistoryInfo.objects.get(province=province,major=major)
        except HistoryInfo.DoesNotExist:
            models.HistoryInfo.objects.create(province=province,major=major)
    data = HistoryInfo.objects.filter(province=province)

    context={'datas': data, 'province': province}
    return render(request,'adminsite/history_info.html',context)

@login_required
def history_edit(request,info_id):
    admin_only(request)
    info = HistoryInfo.objects.get(id=info_id)
    if request.method != 'POST':
        form = HistoryEditForm(instance=info)
    else:
        form = HistoryEditForm(instance=info, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminsite:history_info'))

    context = {'info': info, 'form': form}
    return render(request, 'adminsite/history_edit.html', context)

@login_required
def borderline_predict(request):
    admin_only(request)
    provinces = Province.objects.all()
    curprofile = UserProfile.objects.get(user=request.user)
    default = curprofile.province
    if not default:
        default = 1
    province_id = request.GET.get('province', '')
    if not province_id:
        province_id=default
    history=HistoryInfo.objects.filter(province=province_id)
    curdatas=BorderlinePredict.objects.filter(province=province_id)
    for cur in curdatas:
        cur.delete()
    for his in history:
        lowscore=0
        highscore=1000
        if his.rank is None:
            models.BorderlinePredict.objects.create(major=his.major,lowscore=lowscore,highscore=highscore,province=his.province)
            continue
        rules = RankPredict.objects.filter(province=his.province, sciorart=his.major.sciorart).order_by('score')   #升序扫描
        for rule in rules:
            if rule.lowrank is 0:
                continue
            elif rule.lowrank < his.rank:
                break
            lowscore = rule.score
        rules = RankPredict.objects.filter(province=his.province, sciorart=his.major.sciorart).order_by('-score')  # 降序扫描
        for rule in rules:
            if rule.highrank is None:
                continue
            elif rule.highrank > his.rank:
                break
            highscore = rule.score
        models.BorderlinePredict.objects.create(major=his.major, lowscore=lowscore, highscore=highscore, province=his.province)
    data = BorderlinePredict.objects.filter(province=province_id)


    context = {'datas': data, 'dufault': province_id, 'provinces': provinces, 'default': default}
    return render(request, 'adminsite/borderline_predict.html', context)