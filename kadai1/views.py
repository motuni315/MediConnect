from django. shortcuts import render ,redirect
from django.contrib.auth import authenticate, login


def login(request):
    return render(request,'../templates/kadai1/login/login.html')

def index(request):
    print(request)
    if request.method == "POST":
        userID = request.POST['userID']
        print(userID)
        password = request.POST['password']

        if userID == "admin":
            return render(request,'../templates/kadai1/index/index_admin.html')
        elif userID == "reception":
            return render(request,'../templates/kadai1/index/index_reception.html')
        elif userID == "doctor":
            return render(request,'../templates/kadai1/index/index_doctor.html')

