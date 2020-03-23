from django.shortcuts import render
from .forms import UserCreationForm, PlaceInfoForm
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from django.contrib.auth import logout
from .models import UserProfile
from . import models


# Create your views here.
def register(request):
    if request.method !='POST':
        form=UserCreationForm()
    else:
        form=UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user=form.save()
            return HttpResponseRedirect(reverse('information:index'))

    context={'form':form}
    return render(request,'users/register.html',context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('information:index'))

def place(request):
    cur_id = request.user.id
    try:
        cur = UserProfile.objects.get(user_id=cur_id)
    except UserProfile.DoesNotExist:
        models.UserProfile.objects.create(user_id=cur_id)
    cur = UserProfile.objects.get(user_id=cur_id)
    if request.method!='POST':
        form=PlaceInfoForm(instance=cur)
    else:
        form=PlaceInfoForm(instance=cur,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('information:store_success'))

    context = {'cur': cur, 'form': form}
    return render(request, 'users/place.html', context)