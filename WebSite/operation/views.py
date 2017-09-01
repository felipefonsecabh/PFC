from django.shortcuts import render
from .models import DataDisplay,Registers,OperationMode
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from WebSite.core.tcpclient import Client

try:
    c = Client()
except Exception as err:
    print(str(err))

# Create your views here.
def main(request):
    dp_col = DataDisplay.objects.all()
    #print(dp_col[0].name)
    reg = Registers.objects.latest('pk')
    op = OperationMode.objects.latest('pk')
    context = {
        'dp_col': dp_col,
        'reg':reg,
        'op':op
    }
    return render(request,'operation.html',context)

def refresh(request):

    if request.is_ajax():
        reg = Registers.objects.latest('pk')
        opmode = OperationMode.objects.latest('pk')
        opdata = reg.serialize()
        opdata['OpMode'] = opmode.OpMode

        return JsonResponse(opdata,safe=False)

@csrf_exempt
def command(request):
    if request.is_ajax():
        c.s.sendall(request.POST.get('command').encode('utf-8'))
        msg = 'Sucesso'
        return JsonResponse(msg,safe=False)