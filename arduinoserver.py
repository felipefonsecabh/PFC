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
from multiprocessing import Process, Queue
import asyncore
import socket

#variaveis
start_time = datetime.now()
readinterval = 100
sendDBinterval =1500

#0 para local - comandos via browser não são permitidos, 1 para remoto
arduino_mode = 0   #dado que vem do arduino

#1 para manual- comandos via browser são permitidos, 0 para automatico - comandos via PID
operation_mode = 1   #dado que é enviado do browser, só faz sentido com arduino_mode em remoto
                   #começa com 1 indicando que a operação começa manual

#dicionario que armazena a ultima informação recebida
bstatus = 0
lastdata = {}

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
        mydata['TimeStamp'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        #pegar o modo do arduino
        arduino_mode = mydata['ArduinoMode']      
        parseStatus = True
    else:
        parseStatus = False

    return parseStatus, mydata

#classes para implmmentar o servidor assincrono
class dataHandler(asyncore.dispatcher_with_send):
    
    '''
    def __init__(self,sock,queue):
        self.queue = queue
        self.sock = sock
    '''

    def handle_read(self):
        print(type(self))
        data = self.recv(50)
        '''interpretar os comandos:
        operação: Ligar/Desligar Bomba, Ligar/Desligar Aquecedor, Alterar velocidade da bomba
        Modo: trocar de modo automático para remoto
        Armazenamento: ativar ou desativar o armazenamento de dados para o trend
        '''
        if(data == b'7'):
            operation_mode = 1
            queue.put(data)
            print(data)
        elif(data == b'8'):
            operation_mode = 0
            queue.put(data)
            print(data)
            
        try:
            bytescommand = pack('=cb',data,chksum)
            bus.write_block_data(arduinoAddress,ord(data),list(bytescommand))
        except Exception as err:
            print(str(err))
        finally:
            pass
            #print(data)

class Server(asyncore.dispatcher):

    #queue = None

    def __init__(self,host,port,queue):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.bind((host,port))
        self.listen(1)
        self.queue = queue
    
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
    server = Server('localhost',8080,queue)
    asyncore.loop()

def mainloop(stime,ftime,queue):
    prevmillis = stime
    prevmillis2 = ftime
    operation_mode = 1
    while True:
        try:
            currentmillis2 = millis()
            if(queue.empty):
                pass
            else:
                print('passou')
                operation_mode = queue.get()
                
            if(currentmillis2 - prevmillis2 > readinterval):
                #faz requisicao pelos dados
                #print(operation_mode)
                block = bus.read_i2c_block_data(arduinoAddress,6,27)
                #efetua parse dos dados
                data = unpack('6f3b',bytes(block))
                #print(data)
                bstatus, lastdata = parseData(data)
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

#programa principal
if __name__=='__main__':

    #obtem dados do modelo de registros
    if os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebSite.settings'):
        import django
        django.setup()
        from WebSite.operation.models import Registers
        from django.utils import timezone
    else:
        raise
        sys.exit(1)

    #inicialização do i2c
    bus = SMBus(1)
    arduinoAddress = 12

    prevmillis= millis()       #contador para solicitação de dados para o arduino
    prevmillis2 = prevmillis   #contador para envio do banco

    #cria uma queue para compartilhar variávies do processo
    queue = Queue()

    p1 = Process(target=tcpserver,args=(queue,))
    p1.start()
    p2 = Process(target=mainloop,args=(prevmillis,prevmillis2,queue,))
    p2.start()

    strstatus = 'Servidor rodando'
    print(strstatus)
    


