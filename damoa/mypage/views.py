from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import (authenticate, login as django_login, logout as django_logout)
from django.contrib.auth.models import User
from auction.models import Write, Bid
from django.utils.safestring import mark_safe
import json
from member.models import Profile 


def mymain(request):
    username = request.user.username
    print(request.user.is_authenticated)
    try:
        if request.user.is_authenticated:
            print("1"*10)
            userdata = {
                "username" : request.user.username
                }
                
            loggeduser = request.user.username
            loggedid = request.user.id
            post = Write.objects.filter(writer = loggeduser) #내가 등록한 글
            post2 = Bid.objects.filter(userId_id = loggedid) #내가 입찰한 글
            print(post)
            print(post2)
            print('2'*10)
            info = User.objects.get(id=request.user.id) # 0808 추가
            userinfo = Profile.objects.get(email=info.email) # 0808 추가
            log = request.session.get('log') # 0808 추가
            context = {"userdata":userdata, "post":post, "post2":post2, 'username': mark_safe(json.dumps(username)), 'info':info, 'userinfo':userinfo, 'log':log} # 0808 추가
            return render(request, "mypage/mymain.html", context)
        else:
            return redirect("/")

    except:
        return render(request, "mypage/error.html")


def profileedit(request, id):
    info = get_object_or_404(User, pk=id)
    userinfo = Profile.objects.get(email=info.email)
    loggeduser = request.user.username
    if request.method == "POST":
        userinfo = Profile.objects.get(email=info.email)
        userinfo.name = request.POST['name']
        userinfo.phonenumber = request.POST['phonenumber']
        userinfo.email = request.POST['email']
        userinfo.location = request.POST['location']
        userinfo.save()
        return redirect('mymain')
    else:
        context = {'info':info, 'userinfo':userinfo, 'loggeduser':loggeduser}
        return render(request, 'mypage/proedit.html', context)
    
    
    
    