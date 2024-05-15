from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from kadai1.models import Employee


def login(request):
    return render(request, '../templates/kadai1/login/login.html')


def index(request):
    if request.method == "POST":
        userID = request.POST['userID']
        password = request.POST['password']
        request.session['userID'] = userID

    try:
        emp_info = Employee.objects.get(empid=userID, emppasswd=password)
        request.session['emp_role'] = emp_info.emprole
        print(userID + password)
        if emp_info.emprole == 0:
            return render(request, '../templates/kadai1/index/index_admin.html')
        elif emp_info.emprole == 1:
            return render(request, '../templates/kadai1/index/index_doctor.html')
        elif emp_info.emprole == 2:
            return render(request, '../templates/kadai1/index/index_reception.html')

    except Employee.DoesNotExist:
        return render(request, '../templates/kadai1/login/loginError.html')

