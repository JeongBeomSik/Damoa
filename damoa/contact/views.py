from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Message
from django.contrib.auth.models import User
from .forms import MessageForm
 
 
def sendMessage(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = User.objects.get(username=form.cleaned_data.get("recipient"))
            message.content = form.cleaned_data.get("content")
            message.save()
            return redirect('listMessage')
        else:
            return HttpResponse('해당하는 아이디가 존재하지 않습니다. 다시 확인해주세요.')    
    else:
        form = MessageForm()
        return render(request, 'contact/sendMessage.html', {'form': form})

def listMessage(request):
    messages = Message.objects
    receivedList = Message.objects.filter(recipient=request.user)
    sentList = Message.objects.filter(sender=request.user)
    return render(request, 'contact/listMessage.html', {'messages':messages, 'rlist': receivedList, 'slist': sentList})
    
def viewMessage(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    messages = get_object_or_404(Message, pk=id)
    messages.isRead = True
    messages.save()
    return render(request, 'contact/viewMessage.html', {'messages': messages})

        