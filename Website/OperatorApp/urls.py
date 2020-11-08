from django.urls import path 

from . import views 

app_name = 'operator'

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('edit/', views.edit_profile, name='edit'),
]