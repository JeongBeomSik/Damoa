from django.shortcuts import render, redirect, get_object_or_404
from .models import Group,GroupPurchase
from django.core.paginator import Paginator

def gnew(request):
    loggeduser = request.user.username
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return render(request, 'grouppurchase/new.html', {'loggeduser':loggeduser})

def gcreate(request): # 상품 등록
    if request.method == 'POST':
        post = Group()
        post.writer = request.user.username
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.url = request.POST['url']
        post.recruit = request.POST['recruit']
        post.save()      
        return redirect('gmain')

def gmain(request):
    post = Group.objects
    post_list = Group.objects.all()
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    log = request.session.get('log')
    context = {'post':post, 'posts':posts, 'log':log}
    return render(request, 'grouppurchase/main.html', context)

def gdetail(request, id):
    post = get_object_or_404(Group, pk=id)
    post.lookup = post.lookup + 1
    post.save()
    log = request.session.get('log')
    context = {'post':post, 'log':log}
    return render(request, 'grouppurchase/detail.html', context)

def gupdateordelete(request, id):
    loggeduser = request.user.username
    post = Group.objects.get(pk=id)
    if post.writer == loggeduser:
        if request.POST.get('updateordelete'): # 해당하는 값이 있으면 true, 없으면 false
            post.writer = request.user.username
            post.title = request.POST['title']
            post.content = request.POST['content']
            post.url = request.POST['url']
            post.recruit = request.POST['recruit']
            post.save()
            context = {'post':post}
            return render(request, 'grouppurchase/detail.html', context)
        else:
            post = Group.objects.get(pk=id)
            post.delete()
            return redirect('gmain')

def gupdate(request, id):
    post = Group.objects.get(id=id)
    content = {'post':post}
    return render(request, 'grouppurchase/updateordelete.html', content)