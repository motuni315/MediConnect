from django.http import HttpResponse
from django.shortcuts import render

from kadai1.models import Employee


def login(request):
    return render(request, '../templates/kadai1/L100/login.html')

def logout(request):
    return render(request, '../templates/kadai1/L100/login.html')


def index(request):
    if request.method == "GET":
        userID = request.session.get('userID')

    if request.method == "POST":
        userID = request.POST['userID']
        password = request.POST['password']
        request.session['userID'] = userID

    try:
        emp_info = Employee.objects.get(empid=userID)
        request.session['emp_role'] = emp_info.emprole

        if emp_info.emprole == 0:
            return render(request, '../templates/kadai1/index/index_admin.html')
        elif emp_info.emprole == 1:
            return render(request, '../templates/kadai1/index/index_doctor.html')
        elif emp_info.emprole == 2:
            return render(request, '../templates/kadai1/index/index_reception.html')

    except Employee.DoesNotExist:
        return render(request, '../templates/kadai1/L100/loginError.html')


def register(request):
    if request.method == 'GET':
        return render(request, '../templates/kadai1/admin/E100/emploee_register.html')
    if request.method == 'POST':

        # フォームから送信されたデータを取得
        empid = request.POST['userid']
        empsname = request.POST['surname']
        empfname = request.POST['first-name']
        emppassword = request.POST['password']
        empposition = request.POST['position']

        print(empid, empsname, empfname, emppassword, empposition)

        context = {
            'userid': empid,
            'surname': empsname,
            'first_name': empfname,
            'password': emppassword,
            'position': empposition,
        }

        if Employee.objects.filter(empid=empid).exists():
            return HttpResponse('IDが一致しています')

        return render(request, '../templates/kadai1/admin/E100/emploee_register_confirm.html', context)
    else:
        # GETリクエストの場合は登録フォームを表示
        return render(request, '../templates/kadai1/admin/E100/emploee_register.html')


def confilm_register(request):
    userid = request.POST['userid']
    surname = request.POST['surname']
    first_name = request.POST['first_name']
    password = request.POST['password']
    position = request.POST['position']

    employee = Employee.objects.create(
        empid=userid,
        empfname=surname,
        emplname=first_name,
        emppasswd=password,
        emprole=position
    )

    return render(request,'kadai1/OK.html')


def admin_table(request):
    employees = Employee.objects.all()
    return render(request, '../templates/kadai1/table/admin/employee_table.html', {'employees': employees})


def emp_passChange(request):
    if request.method == 'GET':
        empid = request.GET['empid']
        emppasswd = request.GET['emppasswd']
        return render(request, 'kadai1/admin/E103/employee_passchange.html',{'empid': empid,'emppasswd':emppasswd})

    if request.method == 'POST':
        # POSTリクエストから新しいパスワードを取得
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        empid = request.POST.get('empid')  # 従業員IDを取得する必要があります

        # 新しいパスワードと確認用のパスワードが一致するか確認
        if new_password == confirm_password:
            try:
                # 従業員IDに基づいて従業員情報を取得
                employee = Employee.objects.get(empid=empid)
                # パスワードを更新
                employee.emppasswd = new_password
                employee.save()  # データベースに保存
                return render(request, 'kadai1/OK.html')
            except Employee.DoesNotExist:
                return HttpResponse("指定された従業員IDが見つかりません。")
        else:
            return HttpResponse("新しいパスワードと確認用のパスワードが一致しません。")
    else:
        return render(request, 'kadai1/OK.html')