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

def register(request):
    if request.method == 'GET':
        return render(request, '../templates/kadai1/register/admin/emploee_register.html')
    if request.method == 'POST':
        # フォームから送信されたデータを取得
        userid = request.POST['userid']
        surname = request.POST['surname']
        first_name = request.POST['first-name']
        password = request.POST['password']
        position = request.POST['position']

        # データベースに従業員を登録
        employee = Employee.objects.create(
            empid=userid,
            empfname=surname,
            emplname=first_name,
            emppasswd=password,
            emprole=position
        )

        # 登録情報をemploee_register_confirm.htmlに渡してページ遷移
        return render(request, '../templates/kadai1/register/admin/emploee_register_confirm.html', {'employee': employee})
    else:
        # GETリクエストの場合は登録フォームを表示
        return render(request, '../templates/kadai1/register/admin/emploee_register.html')