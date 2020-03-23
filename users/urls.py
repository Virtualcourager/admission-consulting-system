from django.urls import path, include
from django.contrib.auth.views import LoginView
from . import views
app_name='users'

urlpatterns=[
    path('register', views.register, name='register'),
    path('login/', LoginView.as_view(),name='login'),
    path('logout',views.logout_view,name='logout'),
    path('place',views.place,name='place'),
]