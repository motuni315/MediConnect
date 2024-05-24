from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('index/', views.index, name='index'),
    path('employee_register/', views.employee_register, name='employee_register'),
    path('confilm_register/', views.confilm_register, name='confilm_register'),
    path('admin_table/', views.admin_table, name='admin_table'),
    path('hospital_table/', views.hospital_table, name='hospital_table'),
    path('emp_passChange/', views.emp_passChange, name='emp_passChange'),
    path('phone_change/', views.phone_change, name='phone_change'),
    path('hospital_list/', views.hospital_list, name='hospital_list'),
    path('employee_list/', views.employee_list, name='employee_list'),
    path('patient_register/', views.patient_register, name='patient_register'),
    path('patient_table/', views.patient_table, name='patient_table'),
    path('patient_search/', views.patient_search, name='patient_search'),
    path('insurance_change/', views.insurance_change, name='insurance_change'),
    path('patient_medicine_touyo/',views.patient_medicine_touyo, name='patient_medicine_touyo'),
]
