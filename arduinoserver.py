#!usr/bin/env python3

#import dos módulos necessarios
import serial
import time
import sqlite3
import collections
from datetime import datetime
from datetime import timedelta
from threading import Timer
import os
import sys

'''
def sqlconnect(slqfilepath):
    conn = sqlite3.connect(slqfilepath)
    c = conn.cursor()
    return c

def selectalldata(c):
    c.execute('SELECT * FROM {tn}'.\
        format(tn = table_name))
'''

start_time = datetime.now()

def millis():
    dt = datetime.now()-start_time
    ms = (dt.days*24*60*60 + dt.seconds)*1000+dt.microseconds / 1000.0  
    return ms

#programa principal
if __name__=='__main__':

    import json

    #obtem dados do modelo de registros
    if os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebSite.settings'):
        import django
        django.setup()
        from WebSite.operation.models import Registers
        from django.utils import timezone
    else:
        raise
        sys.exit(1)

    #abertura da porta
    serialport = serial.Serial('/dev/ttyACM0',115200,timeout=1,stopbits=serial.STOPBITS_TWO);
    time.sleep(1);

    #json packet test
    #testjson = 	'{"temps":[5,10,15,20],"flows":[20,10],"status":[0,0,0],"malha_vq":[2,5,102],"malha_vf":[3,11,52]}'

    tests = 0
    #loop

    prevmillis= millis()
    print('Servidor rodando!')
    while True:
        #'''
        #recebe dados da leitura
        receive = serialport.readline()
        receive = receive.decode('utf-8') #necessário para o python3
        #print(receive)
        #verifica se a string recebida consegue ser interpretada corretamente
        try:
            data = json.loads(receive,object_pairs_hook=collections.OrderedDict)  #importar os dados para um dicionário na mesma ordem
        except Exception as err:
            print(str(err))
            #sys.exit()
        else:
            #print json.dumps(data)
            pass
        finally:
            commandstr = '{"commands":[0,0,30]}\n'
            serialport.write(commandstr.encode())
            time.sleep(0.05)  ##concedeu uma consistencia para a comunicação
        #'''
        currentmillis = millis()
        if(currentmillis - prevmillis > 1500):
            #envia dado para o banco de dados
            reg = Registers()
            reg.Temp1 = data['temps'][0]
            reg.Temp2 = data['temps'][1]
            reg.Temp3 = data['temps'][2]
            reg.Temp4 = data['temps'][3]    
            reg.HotFlow = data['flows'][0]
            reg.ColdFlow = data['flows'][1]
            reg.PumpStatus = data['status'][0]
            reg.HeaterStatus = data['status'][2]
            reg.PumpSpeed = data['status'][1]
            reg.TimeStamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            reg.save()
            prevmillis = currentmillis
            
        
        tests = tests+1
        
        #break
          
            #print '1'
            #timestamp
            #para descobrir o tipo da variável -> type(variavel)
            #dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

