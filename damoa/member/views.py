from django.shortcuts import render, redirect
from django.contrib.auth import (authenticate, login as django_login, logout as django_logout)
from django.contrib.auth.models import User
from .forms import UserForm, LoginForm
from .models import Profile
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail



def home(request):
    if not request.user.is_authenticated:
        data = {"username" : request.user, "is_authenticated" : request.user.is_authenticated}
    else:
        data = {"last_login" : request.user.last_login,
            "username" : request.user.username,
            "password" : request.user.password,
            "email" : request.user.email,
            "is_authenticated" : request.user.is_authenticated,
        }
    return render(request, "member/home.html", context={"data" : data})

@csrf_exempt
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        u_id = request.POST.get('u_id')
        pwd = request.POST.get('u_pw')
        user = authenticate(username=u_id, password=pwd)
        if user is not None:
            django_login(request, user)
            log = 1
            request.session['username'] = u_id
            request.session['log'] = log
            return render(request, "mainsite/index.html", {'log' : log})
        else:
            error = "다시 시도해주세요"
            return render(request, "member/login.html", {"form" : form, "error" : error})
    else:
        form = LoginForm()
        return render(request, "member/login.html", {"form" : form})

def logout(request):
    del request.session['username']
    django_logout(request)
    log = 0
    request.session['log'] = log
    request.session.modified = True
    return render(request, "mainsite/index.html", {'log' : log}) 

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        u_id = request.POST.get('u_id')
        cpassword = request.POST.get('cpassword')
        password = request.POST.get('password')
        if form.is_valid() and cpassword == password:
            userdata = Profile()
            userdata.email = request.POST['email'] # 추가됨
            userdata.name = request.POST['name']
            userdata.location = request.POST['location']
            userdata.phonenumber = request.POST['phonenumber']
            userdata.save()
            new_user = User.objects.create_user(**form.cleaned_data)
            django_login(request, new_user)
            log = 1
            request.session['username'] = u_id
            request.session['log'] = log
            return render(request, "mainsite/index.html", {'log' : log})
        else:
            context = {"msg" : "회원가입 실패", "form" : form}
            return render(request, "member/signup.html", context)
    else:
        form = UserForm()
        return render(request, "member/signup.html", {"form" : form})

@csrf_exempt
def findid(request):
    email = request.POST.get('email')
    if request.method == "POST":
        if User.objects.filter(email=email):
            user = User.objects.filter(email=email)
            return render(request, "member/findid.html", {'user':user})
        else:
            error = "다시 시도해주세요"
            return render(request, "member/findid.html", {"error":error})
    return render(request, "member/findid.html")


@csrf_exempt
def findpw(request): # 비밀번호 재설정 페이지
    username = request.POST.get('username')
    email = request.POST.get('email')
    if request.method == "POST":
        if User.objects.filter(email=email, username=username):
            user = User.objects.get(email=email)
            user.password = request.POST['password']
            user.set_password(user.password)
            user.save()
            msg = "비밀번호가 변경되었습니다"
            return render(request, "member/findpw.html", {'user':user, 'msg':msg})
        else:
            error = "다시 시도해주세요"
            return render(request, "member/findpw.html", {"error":error})
    return render(request, "member/findpw.html")



