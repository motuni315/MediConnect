from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('confilm_register/', views.confilm_register, name='confilm_register'),
    path('admin_table/', views.admin_table, name='admin_table'),
    path('emp_passChange/', views.emp_passChange, name='emp_passChange'),
]
