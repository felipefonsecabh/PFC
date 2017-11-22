from django.shortcuts import render
from .models import DataDisplay,Registers,OperationMode
from WebSite.trend.models import TrendRegister
from WebSite.trend.admin import TrendRegisterAdmin
from django.http import HttpResponse, StreamingHttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from WebSite.core.tcpclient import Client
from django.core.exceptions import PermissionDenied
import csv

try:
    c = Client()
except Exception as err:
    print(str(err))

#view para a tela operação. Busca o último dado no banco, insere ao template e envia para requisitante
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

#view para atualizar a tela, é retornado apenas um objeto Json com os dados relativos à última linha do banco.
def refresh(request):

    if request.is_ajax():
        reg = Registers.objects.latest('pk')
        opmode = OperationMode.objects.latest('pk')
        opdata = reg.serialize()
        opdata['OpMode'] = opmode.OpMode
        opdata['TrendStarted'] = opmode.TrendStarted
        return JsonResponse(opdata,safe=False)


#view para enviar um comando para o gateway. É enviado apenas um caractere por um cliente TCP.
@csrf_exempt
def command(request):
    if request.is_ajax():
        c.s.sendall(request.POST.get('command').encode('utf-8'))
        msg = 'Sucesso'
        return JsonResponse(msg,safe=False)

#view para enviar um comando analógico para o gateway. É enviado um pacote Json por um cliente TCP
@csrf_exempt
def analogcommand(request):
    if request.is_ajax():
        speed = request.POST.get('speed')
        jsoncmd  = '{"pump_speed": ' + speed +'}'
        c.s.sendall(jsoncmd.encode('utf-8'))
        msg = 'Sucesso'
        return JsonResponse(msg,safe=False)

def download_csv(modeladmin, request, queryset):
        '''
        if not request.user.is_staff:
            raise PermissionDenied
        '''
        opts = queryset.model._meta
        model = queryset.model
        response = HttpResponse(content_type='text/csv')
        # force download.
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        # the csv writer
        writer = csv.writer(response)
        field_names = [field.name for field in opts.fields]
        # Write a first row with header information
        writer.writerow(field_names)
        # Write data rows
        for obj in queryset:
            writer.writerow([getattr(obj, field, None) for field in field_names])
        return response
        download_csv.short_description = "Download selected as csv"

#view para enviar para o cliente um arquivo csv com o conteúdo da tabela TrendRegister
def exportcsv(request):
    reg = TrendRegister.objects.all()
    data  = download_csv(TrendRegisterAdmin,request,reg)
    response = StreamingHttpResponse(data,content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    return response