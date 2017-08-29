from django.shortcuts import render
from .models import DataDisplay,Registers
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import socket

#criar um cliente socket
class Client():
    def __init__(self,Address=('localhost',8080)):
        self.s = socket.socket()
        self.s.connect(Address)

c = Client()

# Create your views here.
def main(request):
    dp_col = DataDisplay.objects.all()
    #print(dp_col[0].name)
    reg = Registers.objects.latest('pk')
    context = {
        'dp_col': dp_col,
        'reg':reg
    }
    return render(request,'operation.html',context)

def refresh(request):

    if request.is_ajax():
        reg = Registers.objects.latest('pk')
        return JsonResponse(reg.serialize(),safe=False)

@csrf_exempt
def command(request):
    if request.is_ajax():
        c.s.sendall(request.POST.get('command').encode('utf-8'))
        msg = 'Sucesso'
        return JsonResponse(msg,safe=False)