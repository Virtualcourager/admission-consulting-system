from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from django.urls import resolve
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from .models import StuInfor
from .forms import StuInforForms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View

