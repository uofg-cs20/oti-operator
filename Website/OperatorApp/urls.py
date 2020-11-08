from django.urls import path 

from . import views 

app_name = 'operator'

urlpatterns = [
    path('', views.operator_login, name='login'),
    path('logout/', views.operator_logout, name='logout'),
    path('edit/', views.edit_profile, name='edit'),
    path('operators/', views.operators, name='operators'),
    path('api/', views.OperatorView.as_view()),
]