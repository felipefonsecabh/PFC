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

#variaveis
start_time = datetime.now()
readinterval = 60
sendDBinterval = 600
sendTrendDBinterval = 200

#0 para local - comandos via browser não são permitidos, 1 para remoto
arduino_mode = 0   #dado que vem do arduino

#1 para manual- comandos via browser são permitidos, 0 para automatico - comandos via PID
operation_mode = 1   #dado que é enviado do browser, só faz sentido com arduino_mode em remoto
                   #começa com 1 indicando que a operação começa manual

#dicionario que armazena a ultima informação recebida
bstatus = 0
lastdata = {}
lasttrenddata = {}

#informação se é para gravar dados do trend
allow_store_trend_data = 0

#bytechecksum para confirmação
chksum = 15

#variavel para declarar uma tupla vazia

#funções auxiliares
def millis():
    dt = datetime.now()-start_time
    ms = (dt.days*24*60*60 + dt.seconds)*1000+dt.microseconds / 1000.0  
    return ms

def getbit(data,index):
    return(data & (1<<index)!=0)

def parseData(data):
    mydata = {}
    
    if data[8] == 27:
        mydata['Temp1'] = data[0]
        mydata['Temp2'] = data[1]
        mydata['Temp3'] = data[2]
        mydata['Temp4'] = data[3]
        mydata['HotFlow'] = data[4]
        mydata['ColdFlow'] = data[5]
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
        parseStatus = False

    return parseStatus, mydata, trenddata

def process_commands(data):
    #necessário declarar como global, pois está alterando uma variavel dentro da thread
    global operation_mode 
    global allow_store_trend_data

    if(data == b'7'): #set manual
        operation_mode = 1
        #atualizar o registro no ORM
        obj = OperationMode.objects.latest('pk')
        obj.OpMode = operation_mode
        obj.save()

    elif(data == b'8'): #set automatico
        operation_mode = 0
        #atualizar o registro no ORM
        obj = OperationMode.objects.latest('pk')
        obj.OpMode = operation_mode
        obj.save()

    elif(data == b'9'): #start TrendRegister
        allow_store_trend_data = 1
        obj = OperationMode.objects.latest('pk')
        obj.TrendStarted = allow_store_trend_data
        obj.save()

    elif(data == b'A'): #stop TrendRegister
        allow_store_trend_data = 0
        obj = OperationMode.objects.latest('pk')
        obj.TrendStarted = allow_store_trend_data
        obj.save()

    elif(data == b'B'): #clear TrendRegister
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

#classes para implmmentar o servidor assincrono
class dataHandler(asyncore.dispatcher_with_send):
    
    '''
    def __init__(self,sock, addr,queue,server):
        self.SERVER = server
        self.queue = queue
        self.sock = sock
        self.CA = addr
        self.DATA =''
        self.out_buffer =''
        asyncore.dispatcher.__init__(self,sock)
    '''

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
                #print(list(bytescommand))
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
        #self.queue = queue
    
    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            return
        else:
            sock,addr = pair
            #print('Incoming connection from %s' %repr(addr))
            handler = dataHandler(sock)

#classe para implementar a função principal

def tcpserver(queue):
    server = Server('localhost',8080)
    asyncore.loop()

def mainloop(stime,ftime,ttime):
    prevmillis = stime
    prevmillis2 = ftime
    prevmillis3 = ttime
    while True:
        try:
            currentmillis2 = millis()

            '''
            if(queue.empty):
                pass
                #print('vazio')
            else:
                print('passou')
                operation_mode = queue.get()
            '''
            if(currentmillis2 - prevmillis2 > readinterval):
                #faz requisicao pelos dados
                #print(operation_mode)
                block = bus.read_i2c_block_data(arduinoAddress,6,27)
                #efetua parse dos dados
                data = unpack('6f3b',bytes(block))
                #print(data)
                bstatus, lastdata, lasttrenddata = parseData(data)
                #proxima execução
                prevmillis2 = currentmillis2

        except Exception as err:
            print(str(err))

        else:
            '''
            aqui deve-se processar os dados e enviar os comandos caso esteja em 
            modo automatico
            '''             
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

#inicia servidor assincrono
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

    #o armazenamento de dados de trend sempre começa desabilitado
    opMode = OperationMode.objects.latest('pk')
    opMode.TrendStarted  = 0
    opMode.save()

    #inicialização do i2c
    bus = SMBus(1)
    arduinoAddress = 12

    prevmillis= millis()       #contador para solicitação de dados para o arduino
    prevmillis2 = prevmillis   #contador para envio do banco

    loop_thread.daemon = True
    loop_thread.start()
    

    strstatus = 'Servidor rodando'
    print(strstatus)

    #loop principal
    mainloop(prevmillis,prevmillis2,prevmillis)


    #abordagem multi processing
    '''
    #cria uma queue para compartilhar variávies do processo

    queue = Queue()
    p1 = Process(target=tcpserver,args=(queue,))
    p1.start()
    p2 = Process(target=mainloop,args=(prevmillis,prevmillis2,queue,))
    p2.start()
    '''
    
    '''
    manager = Manager()
    q  = manager.Queue
    pool = Pool()
    p1 = pool.apply_async(tcpserver,args=(q,))
    p2 = pool.apply_async(mainloop,args=(prevmillis,prevmillis2,q,))
    '''

 
    


