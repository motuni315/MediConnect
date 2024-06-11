import re
from datetime import datetime

from django.db import models, DatabaseError
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from kadai1.models import Employee, Tabyouin, Patient, Medicine, Treatment, Shiiregyosya


def login(request):
    return render(request, '../templates/kadai1/L100/login.html')


def logout(request):
    if 'userID' in request.session:
        del request.session['userID']
    if 'empinfo' in request.session:
        del request.session['empinfo']
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

        if empposition == '0':
            return HttpResponse('管理者は登録できません。')

        context = {
            'userid': empid,
            'surname': empsname,
            'first_name': empfname,
            'password': emppassword,
            'position': empposition,
        }

        if Employee.objects.filter(empid=empid).exists():
            return HttpResponse('すでに登録されているIDと一致しています')

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


def employee_table(request):
    try:
        employees = Employee.objects.all()
    except DatabaseError:
        return HttpResponse('データベースエラーが発生しました。後でもう一度試してください。')
    return render(request, '../templates/kadai1/admin/E103/employee_table.html', {'employees': employees})


def hospital_table(request):
    try:
        hospitals = Tabyouin.objects.all()
    except DatabaseError:
        return HttpResponse('データベースエラーが発生しました。後でもう一度試してください。')
    return render(request, '../templates/kadai1/admin/H100/hospital_table.html', {'hospitals': hospitals})


def patient_table(request):
    try:
        request.session.pop('deleted_treatments', None)
        request.session.pop('treatment_list', None)
        patients = Patient.objects.all()
    except DatabaseError:
        return HttpResponse('データベースエラーが発生しました。後でもう一度試してください。')
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


import re


def validate_phone_number(phone):
    # 数字のみを抽出
    dig = re.sub(r'[^\d]', '', phone)

    # 電話番号の桁数チェック（例：11桁とする）
    if len(dig) != 11:
        raise ValueError("電話番号は11桁である必要があります。")

    # アルファベットが含まれていないかチェック
    if re.search(r'[a-zA-Z]', phone):
        raise ValueError("電話番号にアルファベットを含めることはできません。")

    # 許可されていないセパレーターが含まれていないかチェック
    if re.search(r'[^\d\-() ]', phone):
        raise ValueError("電話番号には数値、ハイフン、括弧、空白以外の文字を含めることはできません。")

    return phone


def phone_change(request):
    if request.method == 'GET':
        search = int(request.GET['search'])
        request.session['search'] = search

        if search == 1:
            tabyouinid = request.GET['tabyouinid']
            tabyouinmei = request.GET['tabyouinmei']
            tabyouintel = request.GET['tabyouintel']
            context = {
                'tabyouinid': tabyouinid,
                'tabyouinmei': tabyouinmei,
                'tabyouintel': tabyouintel
            }
            return render(request, 'kadai1/admin/H105/phone_change.html',context)
        elif search == 0:
            shiireid = request.GET['shiireid']
            shiiremei = request.GET['shiiremei']
            shiiretel = request.GET['shiiretel']
            context = {
                'shiireid': shiireid,
                'shiiremei': shiiremei,
                'shiiretel': shiiretel
            }
            return render(request, 'kadai1/admin/H105/phone_change.html',context)

    if request.method == 'POST':
        search = request.session.get('search')

        if search == 1:
            hospital_id = request.POST.get('tabyouinid')
            phone = request.POST.get('newPhoneNumber')
        elif search == 0:
            shiire_id = request.POST.get('shiireid')
            phone = request.POST.get('newPhoneNumber')

        try:
            # 電話番号のバリデーション
            validated_phone = validate_phone_number(phone)

            if search == 1:
                hospital = Tabyouin.objects.get(tabyouinid=hospital_id)
                hospital.tabyouintel = validated_phone
                hospital.save()
            elif search == 0:
                shiire = Shiiregyosya.objects.get(shiireid=shiire_id)
                shiire.shiiretel = validated_phone
                shiire.save()
            return render(request, 'kadai1/OK.html')
        except ValueError as ve:
            return HttpResponse(f"エラー: {ve}")
        except Tabyouin.DoesNotExist:
            return HttpResponse("指定された病院IDが見つかりません。")


def normalize_capital_query(query):
    # 数字とカンマ、全角カンマ以外の文字を検出
    if re.search(r'[^\d,，¥￥]', query):
        raise ValueError('無効な文字が含まれています')
    # 数字以外のすべての文字を除去
    return re.sub(r'[^\d]', '', query)


def capital_search(request):
    query = request.GET.get('capital')
    search = request.GET.get('search')

    hospitals = None
    shiires = None

    if query:
        try:
            # 様々な形式の入力を正規化します
            normalized_query = normalize_capital_query(query)
            if normalized_query:  # 数字が残っているか確認します
                capital_value = int(normalized_query)
                if search == '0':
                    hospitals = Tabyouin.objects.filter(tabyouinshihonkin__gte=capital_value)
                elif search == '1':
                    shiires = Shiiregyosya.objects.filter(shihonkin__gte=capital_value)
            else:
                if search == '0':
                    hospitals = Tabyouin.objects.none()
                elif search == '1':
                    shiires = Shiiregyosya.objects.none()
        except ValueError as e:
            return HttpResponse(f'エラー: {e}')
    else:
        if search == '0':
            hospitals = Tabyouin.objects.all()
        elif search == '1':
            shiires = Shiiregyosya.objects.all()

    context = {'hospitals': hospitals,
               'shiires': shiires}

    if search == '0':
        return render(request, 'kadai1/admin/H100/hospital_table.html', context)
    elif search == '1':
        return render(request, 'kadai1/admin/H100/shiire_table.html', context)


def address_search(request):
    address = request.GET.get('address')
    search = request.GET.get('search')

    hospitals = None
    shiires = None

    if address:
        try:
            if search == '0':
                hospitals = Tabyouin.objects.filter(tabyouinaddres__icontains=address)
            elif search == '1':
                shiires = Shiiregyosya.objects.filter(shiireaddress__icontains=address)
        except ValueError as e:
            return HttpResponse(f'エラー: {e}')
    else:
        if search == '0':
            hospitals = Tabyouin.objects.all()
        elif search == '1':
            shiires = Shiiregyosya.objects.all()

    context = {'hospitals': hospitals,
               'shiires': shiires}

    if search == '0':
        return render(request, 'kadai1/admin/H100/hospital_table.html', context)
    elif search == '1':
        return render(request, 'kadai1/admin/H100/shiire_table.html', context)


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
    query = request.GET.get('patient')
    if query:
        # 患者ID、患者名の部分一致検索を実行
        patients = Patient.objects.filter(
            models.Q(patid__icontains=query) | models.Q(patfname__icontains=query) | models.Q(
                patlname__icontains=query))
    else:
        patients = Patient.objects.all()  # クエリがない場合は空のクエリセットを返す

    return render(request, 'kadai1/reception/P103/patient_table.html', {'patients': patients})


def validate_card_number(card_number):
    # 保険証名記号番号の桁数チェック（例：10桁以上とする）
    if len(re.sub(r'[^\d]', '', card_number)) != 10:
        raise ValueError("保険証名記号番号は10桁である必要があります。")

    # アルファベットが含まれていないかチェック
    if re.search(r'[a-zA-Z]', card_number):
        raise ValueError("保険証名記号番号にアルファベットを含めることはできません。")

    # 許可されていないセパレーターが含まれていないかチェック
    if re.search(r'[^\d]', card_number):
        raise ValueError("保険証名記号番号には数値以外の文字を含めることはできません。")

    return card_number


def validate_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.date()
    except ValueError:
        raise ValueError('有効期限は正しい日付形式(YYYY-MM-DD)で入力してください。')


def patient_register(request):
    if request.method == 'GET':
        return render(request, 'kadai1/reception/P101/patient_register.html')
    elif request.method == 'POST':
        pid = request.POST['pid']
        patsname = request.POST['surname']
        patfname = request.POST['first-name']
        insurance_card_number = request.POST['insurance_card_number']
        date_expiry = request.POST['date-expiry']

        try:
            validated_card_number = validate_card_number(insurance_card_number)
            validated_date_expiry = validate_date(date_expiry)
        except ValueError as e:
            return HttpResponse(f'エラー: {e}')

        context = {
            'pid': pid,
            'surname': patsname,
            'first_name': patfname,
            'insurance_card_number': validated_card_number,
            'date_expiry': validated_date_expiry
        }

        if Patient.objects.filter(patid=pid).exists():
            return HttpResponse('すでに登録したIDと一致しています')

        return render(request, 'kadai1/reception/P101/patient_register_confirm.html', context)


def validate_expiry_date(new_date, current_date):
    # new_dateが数値でない場合にエラーを発生させる
    if not isinstance(new_date, str):
        raise TypeError("有効期限は文字列で指定する必要があります。")

    # 新しい有効期限が正しい日付形式であるかどうかをチェック
    try:
        new_date_obj = datetime.strptime(new_date, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError("有効期限の形式が正しくありません。正しい形式はYYYY-MM-DDです。")

    current_date_str = current_date.strftime('%Y-%m-%d')  # current_date を str に変換
    current_date_obj = datetime.strptime(current_date_str, '%Y-%m-%d').date()

    if new_date_obj <= current_date_obj:
        raise ValueError("有効期限は現在の有効期限よりも新しい日付である必要があります。")
    elif new_date_obj == current_date_obj:
        raise ValueError("有効期限は現在の有効期限と同一の日付で変更できません。")

    return new_date_obj

    return new_date_obj


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
        hokenmei = request.POST.get('hokenmei')
        hokenexp = request.POST.get('hokenexp')

        if new_hokenexp:
            try:
                if not new_hokenmei:
                    new_hokenmei = hokenmei
                patient = Patient.objects.get(patid=patid)
                current_expiry = patient.hokenexp
                # 有効期限のバリデーション
                validated_expiry = validate_expiry_date(new_hokenexp, current_expiry)

                # 更新
                patient.hokenmei = new_hokenmei
                patient.hokenexp = validated_expiry
                patient.save()
                return render(request, 'kadai1/OK.html')
            except ValueError as ve:
                return HttpResponse(f"エラー: {ve}")
            except Patient.DoesNotExist:
                return HttpResponse('IDが見つかりません')

        elif new_hokenmei:
            try:
                validated_card_number = validate_card_number(new_hokenmei)

                if new_hokenexp == 'None':
                    new_hokenexp = hokenexp
                patient = Patient.objects.get(patid=patid)
                if new_hokenmei == hokenmei:
                    return HttpResponse("新しい保険証名記号番号は既存のものと同じです。")
                patient.hokenmei = validated_card_number
                patient.save()
                return render(request, 'kadai1/OK.html')
            except Patient.DoesNotExist:
                return HttpResponse('IDが見つかりません')
            except ValueError as e:
                return HttpResponse(f'エラー: {e}')


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

        return render(request, 'kadai1/doctor/medicine_touyo_confirm.html', context)
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
                    'patlname': patlname,
                    'patid': patid
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
                    'patlname': patlname,
                    'patid': patid
                })

        request.session['updated_treatments'] = updated_treatments

        context = {
            'patfname': patfname,
            'patlname': patlname,
            'updated_treatments': updated_treatments,
            'patid': patid

        }
        return render(request, 'kadai1/doctor/medicine_updated.html', context)


def touyo_history(request):
    updated_treatments = request.session.get('updated_treatments')
    return render(request, 'kadai1/doctor/touyo_history.html', {'updated_treatments': updated_treatments})


def history_search(request):
    patients = request.GET.get('patient')
    updated_treatments = request.session.get('updated_treatments')
    if patients:
        # 患者ID、患者名の部分一致検索を実行
        patients = Patient.objects.filter(
            models.Q(patid__icontains=patients) | models.Q(patfname__icontains=patients) | models.Q(
                patlname__icontains=patients))
        if patients.exists():
            updated_treatments = [treatment for treatment in updated_treatments if
                                  treatment.get('patid') in patients.values_list('patid', flat=True)]
        else:
            return HttpResponse('入力された患者IDは見つかりませんでした。')
    else:
        patients = Patient.objects.none()  # クエリがない場合は空のクエリセットを返す

    context = {
        'patients': patients,
        'updated_treatments': updated_treatments
    }
    return render(request, 'kadai1/doctor/touyo_history.html', context)


def hospital_register(request):
    if request.method == 'GET':
        return render(request, 'kadai1/admin/H100/hospital_register.html')
    if request.method == 'POST':
        hospitalid = request.POST.get('hospitalid')
        hospital_name = request.POST.get('hospital_name')
        hospital_number = request.POST.get('hospital_number')
        hospital_address = request.POST.get('hospital_address')
        capital = request.POST.get('capital')
        emergency_response = int(request.POST.get('emergency_response'))

        if Tabyouin.objects.filter(tabyouinid=hospitalid).exists():
            return HttpResponse('エラー: 同じ病院IDが既に存在します。')
        try:
            normalized_query = normalize_capital_query(capital)
            capital_value = int(normalized_query)
            validated_phone = validate_phone_number(hospital_number)

        except ValueError as e:
            return HttpResponse(f'エラー: {e}')

        request.session['hospitalid'] = hospitalid
        request.session['hospital_name'] = hospital_name
        request.session['hospital_number'] = validated_phone
        request.session['hospital_address'] = hospital_address
        request.session['capital'] = capital_value
        request.session['emergency_response'] = emergency_response

        context = {
            'hospitalid': hospitalid,
            'hospital_name': hospital_name,
            'hospital_number': hospital_number,
            'hospital_address': hospital_address,
            'capital': capital,
            'emergency_response': emergency_response
        }
        return render(request, 'kadai1/admin/H100/hopital_register_confirm.html', context)


def hospital_register_confirm(request):
    if request.method == 'POST':
        hospitalid = request.session.get('hospitalid')
        hospital_name = request.session.get('hospital_name')
        hospital_number = request.session.get('hospital_number')
        hospital_address = request.session.get('hospital_address')
        capital = request.session.get('capital')
        emergency_response = int(request.session.get('emergency_response'))

        Tabyouin.objects.create(
            tabyouinid=hospitalid,
            tabyouinmei=hospital_name,
            tabyouintel=hospital_number,
            tabyouinaddres=hospital_address,
            tabyouinshihonkin=capital,
            kyukyu=emergency_response
        )

        del request.session['hospitalid']
        del request.session['hospital_name']
        del request.session['hospital_number']
        del request.session['hospital_address']
        del request.session['capital']
        del request.session['emergency_response']

        return render(request, 'kadai1/OK.html')


def shiire_table(request):
    if request.method == 'GET':
        shiires = Shiiregyosya.objects.all()
        return render(request, 'kadai1/admin/H100/shiire_table.html', {'shiires': shiires})


def shiire_register(request):
    if request.method == 'GET':
        return render(request, 'kadai1/admin/H100/shiire_register.html')
    elif request.method == 'POST':
        shiireid = request.POST.get('shiireid')
        shiiremei = request.POST.get('shiiremei')
        shiireaddress = request.POST.get('shiireaddress')
        shiiretel = request.POST.get('shiiretel')
        shihonkin = request.POST.get('shihonkin')
        nouki = request.POST.get('nouki')

        try:
            nouki = int(nouki)  # 納期が数字の場合のみ変換
        except ValueError:
            return HttpResponse('エラー: 納期は数字で入力してください。')

        if Shiiregyosya.objects.filter(shiireid=shiireid).exists():
            return HttpResponse('エラー: 同じ仕入れ先IDが既に存在します。')
        else:
            normalized_query = normalize_capital_query(shihonkin)
            capital_value = int(normalized_query)
            validated_phone = validate_phone_number(shiiretel)

        # セッションにデータを保存
        request.session['shiireid'] = shiireid
        request.session['shiiremei'] = shiiremei
        request.session['shiireaddress'] = shiireaddress
        request.session['shiiretel'] = shiiretel
        request.session['shihonkin'] = shihonkin
        request.session['nouki'] = nouki

        context = {
            'shiireid': shiireid,
            'shiiremei': shiiremei,
            'shiireaddress': shiireaddress,
            'shiiretel': shiiretel,
            'shihonkin': shihonkin,
            'nouki': nouki
        }

        return render(request, 'kadai1/admin/H100/shiire_register_confirm.html', context)


def shiire_register_confirm(request):
    if request.method == 'POST':
        shiireid = request.session.get('shiireid')
        shiiremei = request.session.get('shiiremei')
        shiireaddress = request.session.get('shiireaddress')
        shiiretel = request.session.get('shiiretel')
        shihonkin = request.session.get('shihonkin')
        nouki = int(request.session.get('nouki'))

        Shiiregyosya.objects.create(
            shiireid=shiireid,
            shiiremei=shiiremei,
            shiireaddress=shiireaddress,
            shiiretel=shiiretel,
            shihonkin=shihonkin,
            nouki=nouki
        )

        del request.session['shiireid']
        del request.session['shiiremei']
        del request.session['shiireaddress']
        del request.session['shiiretel']
        del request.session['shihonkin']
        del request.session['nouki']

        return render(request, 'kadai1/OK.html')


def employee_name_change(request):
    if request.method == 'GET':
        empid = request.GET.get('empid')
        empfname = request.GET.get('empfname')
        emplname = request.GET.get('emplname')

        request.session['empid'] = empid
        request.session['empfname'] = empfname
        request.session['emplname'] = emplname

        context = {
            'empid': empid,
            'empfname': empfname,
            'emplname': emplname
        }
        return render(request, 'kadai1/admin/E103/employee_name_change.html', context)

    elif request.method == 'POST':
        empid = request.session.get('empid')
        empfname = request.session.get('empfname')
        emplname = request.session.get('emplname')
        new_empfname = request.POST.get('new_empfname')
        new_emplname = request.POST.get('new_emplname')

        context = {
            'empid': empid,
            'empfname': empfname,
            'emplname': emplname,
            'new_empfname': new_empfname,
            'new_emplname': new_emplname
        }
        return render(request, 'kadai1/admin/E103/name_change_confirm.html', context)


def name_change_confirm(request):
    empid = request.session.get('empid')
    new_empfname = request.GET.get('new_empfname')
    new_emplname = request.GET.get('new_emplname')

    employee = Employee.objects.get(empid=empid)
    employee.empfname = new_empfname
    employee.emplname = new_emplname
    employee.save()

    return render(request,'kadai1/OK.html')


def check_insurance_expiry(request):
    all = request.GET.get('all')
    expired_patients = Patient.objects.filter(hokenexp__lt=timezone.now())

    if all:
        expired_patients = Patient.objects.all()
    context = {
        'patients': expired_patients,
    }

    return render(request, 'kadai1/reception/P103/patient_table.html', context)
