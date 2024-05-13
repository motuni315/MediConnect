from django. shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse

def login(request):
    return render(request,'../templates/kadai1/login/login.html')

def index(request):
    if request.method == 'post':
        userId = request.POST['userId'],
        password = request.POST['password']
        user = authenticate(request, username=userId, password=password)
        if user is not None:
            login(request, userId)
            if user.admin:
                return HttpResponseRedirect(reverse('admin_dashboard'))  # 管理者画面へ遷移
            elif user.groups.filter(name='Reception').exists():
                return HttpResponseRedirect(reverse('reception_dashboard'))  # 受付画面へ遷移
            elif user.groups.filter(name='Doctor').exists():
                return HttpResponseRedirect(reverse('doctor_dashboard'))  # 医師画面へ遷移
        else:
            # 認証失敗時の処理を追加する場合はここに記述
            pass
        return render(request, 'login.html')  # ログインページを表示