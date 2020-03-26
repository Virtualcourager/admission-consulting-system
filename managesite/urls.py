from django.urls import path
from . import views

app_name='managesite'

urlpatterns=[
    path('account_state/', views.account_state, name='account_state'),
    path('account_edit/<int:user_id>', views.account_edit, name='account_edit'),
    path('major_info/', views.major_info, name='major_info'),
    path('major_edit/<int:major_id>', views.major_edit, name='major_edit'),
]