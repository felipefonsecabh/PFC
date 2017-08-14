from django.shortcuts import render
from .models import DataDisplay,Registers
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers


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
        print(reg)

        #return HttpResponse([reg])
        return JsonResponse(reg.serialize(),safe=False)
