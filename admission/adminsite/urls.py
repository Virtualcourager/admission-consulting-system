from django.urls import path
from . import views
app_name='adminsite'
urlpatterns=[
    path('history_info', views.history_info, name='history_info'),
    path('history_edit/<int:info_id>', views.history_edit, name='history_edit'),
    path('borderline_predict', views.borderline_predict, name='borderline_predict'),
]