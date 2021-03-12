from django.urls import path 

from . import views 

app_name = 'operator'

urlpatterns = [
    path('', views.operator_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.operator_logout, name='logout'),
    path('edit/', views.edit_profile, name='edit'),
    path('operators/', views.operators, name='operators'),
    path('api/operator/', views.OperatorView.as_view()),
    path('api/mode/', views.ModeView.as_view()),
]