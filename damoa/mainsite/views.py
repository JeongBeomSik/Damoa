from django.shortcuts import render
from grouppurchase.models import  GroupPurchase
from auction.models import Write # 경매 db
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
import json

# 7.30 수정
 # 메인사이트를 보여주는 함수 , 추천 항목을 보여줌
def main(request):
    context={}
    contentAuction = Write.objects.all().order_by('-lookup')[:1]  #경매 조회수 상위 2개
    contentGrouppurchase = Write.objects.all().order_by('-lookup')[:1]  #공구 조회수 상위 2개
    username = request.user.username
    log = request.session.get('log')
    context = {'contentAuction': contentAuction, 'contentGrouppurchase':contentGrouppurchase, 'log':log, 'username': mark_safe(json.dumps(username))}        
    return render(request, 'mainsite/index.html', context )

# 통합검색 
def search(request):
    username = request.user.username
    context={}
    log = request.session.get('log')
    # 경매 공구 동시 선택시
    if (request.POST.get('auction') and request.POST.get('grouppurchase')) or (not request.POST.get('auction') and not request.POST.get('grouppurchase')):
        search = request.POST.get('searchbar')
        auction = Write.objects.filter(title__icontains= search)
        grouppurchase = GroupPurchase.objects.filter(id__icontains= search)
        context = {'grouppurchase':  grouppurchase, 'auction': auction, 'log':log,'username': mark_safe(json.dumps(username))}
    # 경매만 선택시    
    elif request.POST.get('auction'):
        search = request.POST.get('searchbar')
        auction = Write.objects.filter(title__icontains= search)
        context = {'auction': auction, 'log':log,'username': mark_safe(json.dumps(username))}
    # 공구만 선택시
    elif request.POST.get('grouppurchase'):
        search = request.POST.get('searchbar')
        grouppurchase = GroupPurchase.objects.filter(id__icontains= search)
        context = {'grouppurchase':  grouppurchase, 'log':log,'username': mark_safe(json.dumps(username))}
    
    return render(request, 'mainsite/searchResult.html', context)
    
        