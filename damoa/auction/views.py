from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Write, Bid, Rating # 0803 추가
from member.models import Profile # 07.28 추가된 곳
from django.contrib.auth.models import User
from django.contrib.auth import authenticate # 07.28 추가된 곳
import json
from django.db.models import Sum # 0807 추가
from django.utils.safestring import mark_safe
import json
# 07.28 수정됨
def new(request): # 상품 등록 페이지
    loggeduser = request.user.username #현재 로그인 중인 사용자 아이디
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    else:
        return render(request, 'auction/new.html', {'loggeduser':loggeduser})
    # !!! new(비로그인시 로그인 페이지로 이동)

def create(request): # 상품 등록
    if request.method == 'POST':
        
        post = Write()
        post.writer = request.user.username
        post.category = request.POST['category'] # 추가됨!!!!
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.buyitnow = request.POST['buyitnow']
        post.up_price = request.POST['up_price']
        post.image = request.FILES['image']
        post.up_date = timezone.datetime.now()
        post.e_date = request.POST['e_date'] # !!! 새로 수정된 곳(기간)
        post.save()
        
        # 08.02 수정됨
        # 07.28 수정됨
        # 현재 로그인 한 유저의 정보는 reqeust 객체 안에 담긴다. request.user.id 로 가져온다
        try:
            if Profile.objects.get(seller=request.user.id): # 현재 로그인 한 유저 아이디 (중복 등록 방지)
                pass    #있으면 pass
        except: # queryset does not exist 예외 처리는 db 에 새로 등록
            add = Profile.objects.get(email=request.user.email)
            add.seller = User.objects.get(id=request.user.id) # 외래키에 자동 삽입 (판매자가 됨)
            add.save()
            
    return redirect(reverse('mainA'))

def delete(request): # 임시로 만듬 (테스트 데이터 삭제)
    post = Write.objects.filter(title='d')
    post.delete()
    return redirect(reverse('mainA'))

def mainA(request): # 등록된 게시글 페이지 !!!새로 수정된 곳 (paginator 적용)
    username = request.user.username
    post = Write.objects
    post_list = Write.objects.all()
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    log = request.session.get('log')
    context = {'post':post, 'posts':posts, 'username': mark_safe(json.dumps(username)), 'log':log}
    return render(request, 'auction/main.html', context)

def detail(request, id):
    username = request.user.username
    post = get_object_or_404(Write, pk=id)
    post.read =True
    post.lookup = post.lookup + 1
    post.save()
    log = request.session.get('log')
    context = {'post':post, 'username': mark_safe(json.dumps(username)), 'log':log}
    return render(request, 'auction/detail.html', context)

#def dataon(request,pk):
    #data = Write.objects.get(pk=pk)
    #print(data+'!!')
    #return render(request, 'new.html',
    #{'data':data})

def bidding(request,id): # !!! 새로 수정된 곳(입찰가 입력관련)
    post = get_object_or_404(Write, pk=id)
    user = User(username=request.user.username)
    if  int(request.GET.get('plus')) >= post.up_price:
        if request.user.is_authenticated:
            price = request.GET.get('plus')
            post.up_price = request.GET.get('plus')
            post.save()
            user = request.user
            user.save()
            print(price)
            b = Bid(userId=user, writerId=post,price=price)
            b.save()
            print(b.id)
            biddings = post.get_biddings()
            print(biddings['li'])
            biddings['li'].append(b.id)
            post.set_biddings(biddings)
            post.save()
            print('post id:',post.id,' biddings: ',biddings['li'])
            # post.biddings.add(user)
            # queryset = post.biddings.all()
            # print(queryset)
            for li in biddings['li']:
                print(Bid.objects.get(id=li).userId , '가 입찰한 가격은 ',
                Bid.objects.get(id=li).price,'원 입니다')
            context = {'post':post}
            return render(request, 'auction/detail.html', context)
        else:
            return redirect(reverse('mainA'))
    else:
        context = {'post':post}
        return render(request, 'auction/detail.html', context)

def fastpurchase(request,id):
    return render(request,'auction/fastpurchase.html')

def writerinfo(request, id): # 0807 수정
    #판매자 정보
    post = get_object_or_404(Write, pk=id)
    seller = post.writer
    info = User.objects.get(username=seller)
    info2 = Profile.objects.get(seller=info.id)
    pseller = info2.seller
    rateall = ""
    rate = ""
    if request.method == "POST":
        g = request.POST.get('g')
        c = request.POST.get('c')
        newrate = pseller.rating_set.create(seller=pseller, grade=g, comment=c)
    if Rating.objects.filter(seller=pseller):
        rateall = Rating.objects.filter(seller=pseller)
        count = Rating.objects.filter(seller=pseller).count() 
        rsum = Rating.objects.filter(seller=pseller).aggregate(Sum('grade'))
        rate = round(rsum['grade__sum']/count, 2)
    log = request.session.get('log')
    context = {'post':post, 'seller':seller, 'info':info, 'info2':info2, 'rateall':rateall, 'rate':rate, 'log':log}
    return render(request,'auction/writerinfo.html', context)


# 0803 추가

def updateordelete(request, id):
    loggeduser = request.user.username
    post = Write.objects.get(pk=id)
    if post.writer == loggeduser:
        if request.POST.get('updateordelete'): # 해당하는 값이 있으면 true, 없으면 false
            post.writer = request.user.username
            post.category = request.POST['category']
            post.title = request.POST['title']
            post.content = request.POST['content']
            post.buyitnow = request.POST['buyitnow']
            post.up_price = request.POST['up_price']
            post.image = request.FILES['image']
            post.up_date = timezone.datetime.now()
            post.e_date = request.POST['e_date'] # !!! 새로 수정된 곳(기간)
            post.save()
            context = {'post':post}
            return render(request, 'auction/detail.html', context)
        else:
            post = Write.objects.get(pk=id)
            post.delete()
            return redirect('mainA')

def update(request, id):
    post = Write.objects.get(id=id)
    content = {'post':post}
    return render(request, 'auction/updateordelete.html', content)