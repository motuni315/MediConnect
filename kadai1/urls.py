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
    path('add_medicine/', views.add_medicine, name='add_medicine'),
    path('delete_medicine/', views.delete_medicine, name='delete_medicine'),
    path('medicine_touyo_confirm/',views.medicine_touyo_confirm, name='medicine_touyo_confirm'),
    path('touyo_history/',views.touyo_history, name='touyo_history'),
    path('history_search/', views.history_search, name='history_search'),
]
