from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from kadai1.models import Employee, Tabyouin, Patient, Medicine, Treatment


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
    request.session.pop('deleted_treatments', None)
    request.session.pop('treatment_list', None)
    patients = Patient.objects.all()
    return render(request, 'kadai1/reception/P103/patient_table.html', {'patients': patients})


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
        return render(request, 'kadai1/admin/H105/phone_change.html',
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


def insurance_change(request):
    if request.method == 'GET':
        patid = request.GET.get('patid')
        hokenmei = request.GET.get('hokenmei')
        hokenexp = request.GET.get('hokenexp')
        check = request.GET.get('check')

        check = int(check)

        context = {
            'patid': patid,
            'hokenmei': hokenmei,
            'hokenexp': hokenexp,
            'check': check
        }
        return render(request, 'kadai1/reception/P104/insurance_change.html', context)
    elif request.method == 'POST':
        patid = request.POST.get('patid')
        new_hokenmei = request.POST.get('new_hokenmei')
        new_hokenexp = request.POST.get('new_hokenexp')

        if new_hokenmei:
            try:
                patient = Patient.objects.get(patid=patid)
                patient.hokenmei = new_hokenmei
                patient.save()
                return render(request, 'kadai1/OK.html')
            except Patient.DoesNotExist:
                return HttpResponse('IDが見つかりません')

        elif new_hokenexp:
            try:
                patient = Patient.objects.get(patid=patid)
                patient.hokenexp = new_hokenexp
                patient.save()
                return render(request, 'kadai1/OK.html')
            except Patient.DoesNotExist:
                return HttpResponse('IDが見つかりません')


def patient_medicine_touyo(request):
    if request.method == 'GET':
        patid = request.GET.get('patid')
        patfname = request.GET.get('patfname')
        patlname = request.GET.get('patlname')
        treatments = Treatment.objects.filter(patid=patid).select_related('medicineid')
        medicines = Medicine.objects.all()  # 全件取得

        request.session['patid'] = patid  # セッション登録
        request.session['patfname'] = patfname
        request.session['patlname'] = patlname

        treatmement_list = []
        for treatment in treatments:
            treatmement_list.append({
                'id': treatment.id,
                'quantity': treatment.quantity,
                'medicinename': treatment.medicineid.medicinename,
                'medicineid': treatment.medicineid.medicineid
            })

        request.session['treatment_list'] = treatmement_list

        context = {
            'patid': patid,
            'patfname': patfname,
            'patlname': patlname,
            'treatments': treatmement_list,
            'medicines': medicines
        }
        return render(request, 'kadai1/doctor/patient_medicine_touyo.html', context)


def add_medicine(request):
    if request.method == 'POST':
        medicineid = request.POST.get('medicineid')
        patid = request.session.get('patid')
        patfname = request.session.get('patfname')
        patlname = request.session.get('patlname')
        quantity = request.POST.get('quantity')
        medicines = Medicine.objects.all()

        medicine = Medicine.objects.get(medicineid=medicineid)
        treatment_list = request.session.get('treatment_list', [])

        # Check if the medicineid is already in the treatment_list
        if not any(item['medicineid'] == medicineid for item in treatment_list):
            treatment_list.append({
                'quantity': int(quantity),  # Use the quantity from the POST data
                'medicinename': medicine.medicinename,
                'medicineid': medicine.medicineid,
            })
        else:
            # If the medicineid is in the treatment_list, update the quantity
            for item in treatment_list:
                if item['medicineid'] == medicineid:
                    item['quantity'] += int(quantity)

        # Save the updated treatment_list to the session
        request.session['treatment_list'] = treatment_list

        context = {
            'patid': patid,
            'patfname': patfname,
            'patlname': patlname,
            'treatments': treatment_list,
            'medicines': medicines
        }

        return render(request, 'kadai1/doctor/patient_medicine_touyo.html', context)


def delete_medicine(request):
    if request.method == 'POST':
        medicineid = request.POST.get('medicineid')
        patid = request.session.get('patid')
        patfname = request.session.get('patfname')
        patlname = request.session.get('patlname')
        quantity = int(request.POST.get('quantity'))  # quantity を整数として取得
        medicines = Medicine.objects.all()

        # セッションから treatment_list と deleted_treatments を取得
        treatment_list = request.session.get('treatment_list', [])
        deleted_treatments = request.session.get('deleted_treatments', [])
        # treatment_listのmedicineidと入力したmedicineidが一致するレコードを抽出する
        treatment_info = [t for t in treatment_list if t['medicineid'] == medicineid]

        if not deleted_treatments:  # リストが空だった時にリストに追加
            for treatment in treatment_info:
                if 'id' in treatment:
                    deleted_treatments.append({
                        'quantity': treatment['quantity'],
                        'medicineid': medicineid,
                        'id': treatment['id']
                    })
                else:
                    deleted_treatments.append({
                        'quantity': treatment['quantity'],
                        'medicineid': medicineid,
                    })
        elif not any(item['medicineid'] == medicineid for item in deleted_treatments):
            for treatment in treatment_info:
                if 'id' in treatment:
                    deleted_treatments.append({
                        'quantity': treatment['quantity'],
                        'medicineid': medicineid,
                        'id': treatment['id']
                    })
                else:
                    deleted_treatments.append({
                        'quantity': treatment['quantity'],
                        'medicineid': medicineid,
                    })

        for deleted_treatment in deleted_treatments:
            if deleted_treatment['medicineid'] == medicineid:
                deleted_treatment['quantity'] -= quantity

                if deleted_treatment['quantity'] <= 0:
                    deleted_treatment['quantity'] = 0

                for treatment_lists in treatment_list:
                    if treatment_lists['medicineid'] == deleted_treatment['medicineid']:
                        treatment_lists['quantity'] = deleted_treatment['quantity']

                if deleted_treatment['quantity'] == 0:
                    deleted_treatments.remove(deleted_treatment)

        request.session['deleted_treatments'] = deleted_treatments

        context = {
            'patid': patid,
            'patfname': patfname,
            'patlname': patlname,
            'treatments': treatment_list,
            'medicines': medicines,
        }
        return render(request, 'kadai1/doctor/patient_medicine_touyo.html', context)


def medicine_touyo_confirm(request):
    if request.method == 'GET':
        patfname = request.session.get('patfname')
        patlname = request.session.get('patlname')
        treatments = request.session.get('treatment_list')

        context = {
            'patfname': patfname,
            'patlname': patlname,
            'treatments': treatments,
        }

        return render(request, 'kadai1/doctor/medicine_touyo_confirm.html',context)
    if request.method == 'POST':
        patfname = request.session.get('patfname')
        patlname = request.session.get('patlname')
        treatments = request.session.get('treatment_list')
        impdate = timezone.now().date()
        patid = request.session.get('patid')
        updated_treatments = request.session.get('updated_treatments', [])
        # 保存した情報を格納する新しいリスト

        for treatment in treatments:
            treatment_id = treatment.get('id')
            if treatment_id:
                # IDが存在する場合は更新
                treatment_record = Treatment.objects.get(id=treatment_id)
                treatment_record.medicinename = treatment['medicinename']
                treatment_record.quantity = treatment['quantity']
                treatment_record.impdate = impdate
                treatment_record.save()

                updated_treatments.append({
                    'id': treatment_record.id,
                    'medicinename': treatment_record.medicinename,
                    'quantity': treatment_record.quantity,
                    'impdate': impdate.strftime("%Y-%m-%d"),
                    'patfname': patfname,
                    'patlname': patlname
                })
            else:
                medicine_id = treatment['medicineid']
                medicine_instance = Medicine.objects.get(medicineid=medicine_id)
                # IDが存在しない場合は新しいレコードを作成
                new_treatment = Treatment.objects.create(
                    medicineid=medicine_instance,
                    quantity=treatment['quantity'],
                    patid=patid,  # 患者IDをセッションから取得
                    impdate=impdate
                )

                updated_treatments.append({
                    'id': new_treatment.id,
                    'medicinename': medicine_instance.medicinename,
                    'quantity': new_treatment.quantity,
                    'impdate': impdate.strftime("%Y-%m-%d"),
                    'patfname': patfname,
                    'patlname': patlname
                })

        request.session['updated_treatments'] = updated_treatments

        context = {
            'patfname': patfname,
            'patlname': patlname,
            'updated_treatments': updated_treatments

        }
        return render(request,'kadai1/doctor/medicine_updated.html',context)