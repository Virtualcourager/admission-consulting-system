from django.urls import path
from . import views

app_name='informations'

urlpatterns=[
    path('', views.index, name='index'),
    path('new_stu/', views.new_stu, name='new_stu'),
    path('store_success/', views.store_success, name='store_success'),
    path('store_failed/', views.store_failed, name='store_failed'),
    path('search_info/', views.search_info, name='search_info'),
    path('edit_info/<int:info_id>/<int:info_testnum>', views.edit_info, name='edit_info'),
    path('admin_display', views.admin_display, name='admin_display'),
    path('admin_edit/<int:info_id>',views.admin_edit,name='admin_edit'),
    path('output',views.output,name='output'),
    path('down', views.down, name='down'),
    path('rank_display/', views.rank_display, name='rank_display'),
]