#!usr/bin/env python3

#import dos módulos necessarios
import time
import collections
from datetime import datetime
from datetime import timedelta
from threading import Timer
import os
import sys
from smbus import SMBus
from struct import pack, unpack
import threading
from multiprocessing import Process, Queue, Manager,Pool
import asyncore
import socket
import json
import timeit

#variaveis
start_time = datetime.now()
readinterval = 300
sendDBinterval = 500
sendTrendDBinterval = 500

#0 para local - comandos via browser não são permitidos, 1 para remoto
arduino_mode = 0   #dado que vem do arduino

#1 para manual- comandos via browser são permitidos, 0 para automatico - comandos via PID
operation_mode = 1   #dado que é enviado do browser, só faz sentido com arduino_mode em remoto
                   #começa com 1 indicando que a operação começa manual

#dicionario que armazena a ultima informação recebida
bstatus = 0
lastdata = {}
lasttrenddata = {}
lastvaliddata = {}
lastvalidtrenddata = {}
databuffer = [0] * 7

#informação se é para gravar dados do trend
allow_store_trend_data = 0

#bytechecksum para confirmação
chksum = 15


#funções auxiliares
def initialize():
    lastdata['Temp1'] = 0
    lastdata['Temp2'] = 0
    lastdata['Temp3'] = 0
    lastdata['Temp4'] = 0
    lastdata['HotFlow'] = 0
    lastdata['ColdFlow'] = 0
    lastdata['PumpSpeed'] = 0
    lastdata['PumpStatus'] = 0
    lastdata['HeaterStatus'] = 0
    lastdata['ArduinoMode'] = 0
    lastdata['EmergencyMode'] = 0
    lastdata['TimeStamp'] = 0

def millis():
    dt = datetime.now()-start_time
    ms = (dt.days*24*60*60 + dt.seconds)*1000+dt.microseconds / 1000.0  
    return ms

def getbit(data,index):
    return(data & (1<<index)!=0)

def parseData(data):
    mydata = {}
    
    if data[8] == 27:
        global ReadingErrors
        global lastdata
        global lasttrenddata

        #Filtrar Spikes
        SpikeFilter(data)

        mydata['Temp1'] = databuffer[0]     #databuffer[0]
        mydata['Temp2'] = databuffer[1]     #databuffer[1]  
        mydata['Temp3'] = databuffer[3]     #databuffer[2]
        mydata['Temp4'] = databuffer[2]     #databuffer[3]
        mydata['HotFlow'] = databuffer[4]   #databuffer[4]
        mydata['ColdFlow'] = databuffer[5]  #databuffer[5]
        mydata['PumpSpeed'] = data[6]
        mydata['PumpStatus'] = getbit(data[7],0)
        mydata['HeaterStatus'] = getbit(data[7],1)
        mydata['ArduinoMode'] = getbit(data[7],2)
        mydata['EmergencyMode'] = getbit(data[7],3)
        mydata['TimeStamp'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        #pegar o modo do arduino
        arduino_mode = mydata['ArduinoMode']
    
        trenddata = dict([(x, mydata[x]) for x in ['Temp1', 'Temp2', 'Temp3','Temp4','HotFlow','ColdFlow','PumpSpeed','TimeStamp']])  
        parseStatus = True
    else:
        mydata = 'error'
        trenddata = 'error'
        parseStatus = False
        ReadingErrors = ReadingErrors + 1
        #print('Reading Errors: %f',ReadingErrors)

    return parseStatus, mydata, trenddata

def SpikeFilter(data):
    #filtro para temperatura
    global SpikeErrors
    
    for i in range(0,4):
        if(data[i] < 0.0):
            SpikeErrors = SpikeErrors + 1
        elif((abs(data[i] - databuffer[i]) > 10) and (databuffer[i] != 0)):
            SpikeErrors = SpikeErrors + 1
        else:  #dado normal
            databuffer[i] = data[i]
    
    #filtro para a vazao quente
    if(data[4]<0.0):
        SpikeErrors = SpikeErrors + 1
    elif((abs(databuffer[4] - data[4]) > 5) and (databuffer[4] > 0)): #spike
        SpikeErrors = SpikeErrors + 1
    else: # normal
        databuffer[4] = data[4]

    #filtro para a vazao fria
    if(data[5]<0.0):
        SpikeErrors = SpikeErrors + 1
    elif((abs(databuffer[5] - data[5]) > 5) and (databuffer[5] > 0)): #spike
        SpikeErrors = SpikeErrors + 1
    else: # normal
        databuffer[5] = data[5]
    
    
def process_commands(data):
    #necessário declarar como global, pois está alterando uma variavel dentro da thread
    global operation_mode 
    global allow_store_trend_data

    #comandos de controle do gateway
    if(data == b'7'): #start TrendRegister
        allow_store_trend_data = 1
        obj = OperationMode.objects.latest('pk')
        obj.TrendStarted = allow_store_trend_data
        obj.save()

    elif(data == b'8'): #stop TrendRegister
        allow_store_trend_data = 0
        obj = OperationMode.objects.latest('pk')
        obj.TrendStarted = allow_store_trend_data
        obj.save()

    elif(data == b'9'): #clear TrendRegister
        try:
            tdata = TrendRegister.objects.all().delete()
        except Exception as err:
            print(str(err))

    else: #comandos para enviar para o arduino
        try:
            bytescommand = pack('=cb',data,chksum)
            bus.write_block_data(arduinoAddress,ord(data),list(bytescommand))
        except Exception as err:
            print(str(err))
        finally:
            pass         
            #print(data)
    
    ''' o modo manual e automatico não está implementado ainda
    elif(data == b'A'): #set manual
        operation_mode = 1
        #atualizar o registro no ORM
        obj = OperationMode.objects.latest('pk')
        obj.OpMode = operation_mode
        obj.save()

    elif(data == b'B'): #set automatico
        operation_mode = 0
        #atualizar o registro no ORM
        obj = OperationMode.objects.latest('pk')
        obj.OpMode = operation_mode
        obj.save()
    '''

#classes para implmmentar o servidor assincrono
class dataHandler(asyncore.dispatcher_with_send):
    
    def handle_read(self):
        
        data = self.recv(50)

        '''interpretar os comandos:
        operação: Ligar/Desligar Bomba, Ligar/Desligar Aquecedor, Alterar velocidade da bomba
        Modo: trocar de modo automático para remoto
        Armazenamento: ativar ou desativar o armazenamento de dados para o trend e
        também apagar dados
        '''
        if len(data) < 2:  #comandos digitais
            process_commands(data)
        else: #comando analogico
            try:
                ld = json.loads(data.decode('utf-8'))
                bytescommand = pack('f',ld['pump_speed'])
                bus.write_block_data(arduinoAddress,53,list(bytescommand))
            except Exception as err:
                print(str(err))
            finally:
                pass
                
class Server(asyncore.dispatcher):

    #queue = None
    def __init__(self,host,port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.bind((host,port))
        self.listen(1)
    
    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            return
        else:
            sock,addr = pair
            handler = dataHandler(sock)

def tcpserver(queue):
    server = Server('localhost',8080)
    asyncore.loop()

#função principal
def mainloop(initialtime):
    prevmillis = initialtime
    prevmillis2 = initialtime
    prevmillis3 = initialtime
    while True:
        try:
            currentmillis2 = millis()

            if(currentmillis2 - prevmillis2 > readinterval):
                
                #proxima execução
                prevmillis2 = currentmillis2

                #faz requisicao pelos dados
                block = bus.read_i2c_block_data(arduinoAddress,54,30)

                #transforma o array de bytes em variáveis
                data = unpack('7f2b',bytes(block))

                #armazena as variáveis em um dicionário
                bstatus, data, trendata = parseData(data)
                if(bstatus):
                        lastdata = data
                        lasttrenddata = trendata
        except Exception as err:
            print(str(err))            
        finally:
            currentmillis = millis()
            if(currentmillis - prevmillis > sendDBinterval):
                #envia dado para o banco de dados (lastdata contém últimos dados válidos)
                reg = Registers(**lastdata)
                reg.save()
            
                #proxima execução
                prevmillis = currentmillis
            
            currentmillis3 = millis()
            if(currentmillis3 - prevmillis3 > sendTrendDBinterval):
                
                if(allow_store_trend_data):
                    #envia dado para o banco de dados
                    treg = TrendRegister(**lasttrenddata)
                    treg.save()
                    #próxima execução
                    prevmillis3 = currentmillis3
                else:
                    pass

#configura servidor assíncrono
server = Server('localhost', 8080)
loop_thread = threading.Thread(target=asyncore.loop, name='AsyncoreLoop')

#programa principal
if __name__=='__main__':

    #obtem dados do modelo de registros
    if os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebSite.settings'):
        import django
        django.setup()
        from WebSite.operation.models import Registers, OperationMode
        from WebSite.trend.models import TrendRegister
        from django.utils import timezone
    else:
        raise
        sys.exit(1)
    

    #apagar os dados do banco trend sempre que incializar
    try:
        tdata = TrendRegister.objects.all().delete()
        rdata = Registers.objects.all().delete()
    except Exception as err:
        print(str(err))

    #variável para armazenar o númmero de erros de leitura
    ReadingErrors = 0
    SpikeErrors = 0

    #o armazenamento de dados de trend sempre começa desabilitado
    opMode = OperationMode.objects.latest('pk')
    opMode.TrendStarted  = 0  #para começar habilitado basta trocar para 1
    opMode.save()

    #inicialização do i2c
    bus = SMBus(1)
    arduinoAddress = 12

    initialize()  #inicializa estrutura de armazenamento de dados

    #inicia servidor TCP assincrono em outra thread
    loop_thread.daemon = True  
    loop_thread.start()
    
    strstatus = 'Servidor rodando'
    print(strstatus)

    #loop principal
    mainloop(millis())
 
    


