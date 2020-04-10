from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth.views import LoginView
from admission.settings import MEDIA_ROOT
from django.views.static import serve
from . import views
app_name='material'

urlpatterns=[
    path('upload', views.upload, name='upload'),
    url(r'^file/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT},name='file'),
    path('file_display', views.file_display , name='file_display'),
    path('file_summary',views.file_summary, name='file_summary')
]