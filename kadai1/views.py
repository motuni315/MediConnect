from django.http import HttpResponse
from django.shortcuts import render

from kadai1.models import Employee, Tabyouin, Patient


def login(request):
    return render(request, '../templates/kadai1/L100/login.html')


def logout(request):
    request.session.flush()
    return render(request, '../templates/kadai1/L100/login.html')


def index(request):
    if request.method == "GET":
        userID = request.session.get('userID')

        emp_info = Employee.objects.get(empid=userID)

        if emp_info.emprole == 0:
            return render(request, '../templates/kadai1/index/index_admin.html')
        elif emp_info.emprole == 1:
            return render(request, '../templates/kadai1/index/index_doctor.html')
        elif emp_info.emprole == 2:
            return render(request, '../templates/kadai1/index/index_reception.html')

    if request.method == "POST":
        userID = request.POST['userID']
        password = request.POST['password']
        request.session['userID'] = userID

    try:
        emp_info = Employee.objects.get(empid=userID, emppasswd=password)
        request.session['emprole'] = emp_info.emprole
    except Employee.DoesNotExist:
        return render(request, '../templates/kadai1/L100/loginError.html')

    if emp_info.emprole == 0:
        return render(request, '../templates/kadai1/index/index_admin.html')
    elif emp_info.emprole == 1:
        return render(request, '../templates/kadai1/index/index_doctor.html')
    elif emp_info.emprole == 2:
        return render(request, '../templates/kadai1/index/index_reception.html')


def employee_register(request):
    if request.method == 'GET':
        return render(request, '../templates/kadai1/admin/E101/emploee_register.html')
    if request.method == 'POST':


        # フォームから送信されたデータを取得
        empid = request.POST['userid']
        empsname = request.POST['surname']
        empfname = request.POST['first-name']
        emppassword = request.POST['password']
        empposition = request.POST['position']

        context = {
                'userid': empid,
                'surname': empsname,
                'first_name': empfname,
                'password': emppassword,
                'position': empposition,
            }

        if Employee.objects.filter(empid=empid).exists():
            return HttpResponse('IDが一致しています')

        return render(request, '../templates/kadai1/admin/E101/emploee_register_confirm.html', context)



def confilm_register(request):
    emprole = request.session.get('emprole')
    if emprole == 0:
        userid = request.POST['userid']
        surname = request.POST['surname']
        first_name = request.POST['first_name']
        password = request.POST['password']
        position = request.POST['position']

        Employee.objects.create(
            empid=userid,
            empfname=surname,
            emplname=first_name,
            emppasswd=password,
            emprole=position
        )
    elif emprole == 2:
        patid = request.POST['patid']
        patfname = request.POST['patfname']
        patlname = request.POST['patlname']
        hokenmei = request.POST['hokenmei']
        hokenexp = request.POST['hokenexp']

        Patient.objects.create(
            patid=patid,
            patfname=patfname,
            patlname=patlname,
            hokenmei=hokenmei,
            hokenexp=hokenexp

        )

    return render(request, 'kadai1/OK.html')


def admin_table(request):
    employees = Employee.objects.all()
    return render(request, '../templates/kadai1/admin/E103/employee_table.html', {'employees': employees})


def hospital_table(request):
    hospitals = Tabyouin.objects.all()
    return render(request, '../templates/kadai1/admin/H100/hospital_table.html', {'hospitals': hospitals})

def patient_table(request):
    patients = Patient.objects.all()
    return render(request,'kadai1/reception/P103/patient_table.html',{'patients': patients})


def emp_passChange(request):
    if request.method == 'GET':
        emprole = request.session['emprole']

        if emprole == 0:
            empid = request.GET['empid']
            emppasswd = request.GET['emppasswd']
            return render(request, 'kadai1/admin/E103/employee_passchange.html',
                          {'empid': empid, 'emppasswd': emppasswd})
        else:
            empid = request.session.get('userID')
            emp_info = Employee.objects.get(empid=empid)
            emppasswd = emp_info.emppasswd

            return render(request, 'kadai1/reception/reception_emploee_change.html',
                          {'empid': empid, 'emppasswd': emppasswd})

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


def phone_change(request):
    if request.method == 'GET':
        tabyouinid = request.GET['tabyouinid']
        tabyouintel = request.GET['tabyouintel']
        return render(request, 'kadai1/update/phone_change.html',
                      {'tabyouinid': tabyouinid, 'tabyouintel': tabyouintel})

    if request.method == "POST":
        hospital_id = request.POST.get('tabyouinid')
        hospital_phone = request.POST.get('newPhoneNumber')

        try:
            hospital = Tabyouin.objects.get(tabyouinid=hospital_id)

            hospital.tabyouintel = hospital_phone
            hospital.save()
            return render(request, 'kadai1/OK.html')
        except Tabyouin.DoesNotExist:
            return HttpResponse("指定された病院IDが見つかりません。")


def hospital_list(request):
    query = request.GET.get('capital')
    if query:
        try:
            capital_value = int(query)
            hospitals = Tabyouin.objects.filter(tabyouinshihonkin__gte=capital_value)
        except ValueError:
            hospitals = Tabyouin.objects.none()
    else:
        hospitals = Tabyouin.objects.all()

    context = {'hospitals': hospitals}
    return render(request, '../templates/kadai1/admin/H100/hospital_table.html', context)


def employee_list(request):
    employee = request.GET.get('employee')
    if employee:
        try:
            emp_info = Employee.objects.filter(empid=employee)
        except ValueError:
            emp_info = Employee.objects.all()
    else:
        emp_info = Employee.objects.all()
    context = {'employees': emp_info}
    return render(request, 'kadai1/admin/E103/employee_table.html', context)

def patient_search(request):
    patient = request.GET.get('patient')
    if patient:
        patients = Patient.objects.filter(patid__icontains=patient)
    else:
        patients = Patient.objects.none()  # クエリがない場合は空のクエリセットを返す

    return render(request, 'kadai1/reception/P103/patient_table.html', {'patients': patients})

def patient_register(request):
    if request.method == 'GET':
        return render(request, 'kadai1/reception/P101/patient_register.html')
    elif request.method == 'POST':
        pid = request.POST['pid']
        patsname = request.POST['surname']
        patfname = request.POST['first-name']
        insurance_card_number = request.POST['insurance_card_number']
        date_expiry = request.POST['date-expiry']

        context = {
            'pid': pid,
            'surname': patsname,
            'first_name': patfname,
            'insurance_card_number': insurance_card_number,
            'date_expiry': date_expiry
        }

        if Patient.objects.filter(patid=pid).exists():
            return HttpResponse('IDが一致しています')

        return render(request, 'kadai1/reception/P101/patient_register_confirm.html', context)
