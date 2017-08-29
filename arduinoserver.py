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
parseStatus = False
readinterval = 100
sendDBinterval =1500

#bytechecksum para confirmação
chksum = 15

def millis():
    dt = datetime.now()-start_time
    ms = (dt.days*24*60*60 + dt.seconds)*1000+dt.microseconds / 1000.0  
    return ms

def getbit(data,index):
    return(data & (1<<index)!=0)

#classes para implmmentar o servidor assincrono
class dataHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(50)
        
        #digital commands
        try:
            bytescommand = pack('=cb',data,chksum)
            bus.write_block_data(arduinoAddress,ord(data),list(bytescommand))
        except Exception as err:
            print(str(err))
        finally:
            pass
            #print(data)

class Server(asyncore.dispatcher):
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
            #print('Incoming connection from %s' %repr(addr))
            handler = dataHandler(sock)

server = Server('localhost',8080)

#classe para implementar a função principal

def mainloop(stime,ftime):
    prevmillis = stime
    prevmillis2 = ftime
    while True:
        try:
            currentmillis2 = millis()
            if(currentmillis2 - prevmillis2 > readinterval):
                #faz requisicao pelos dados
                block = bus.read_i2c_block_data(arduinoAddress,6,27)
                #efetua parse dos dados
                data = unpack('6f3b',bytes(block))
                #print(data)
                if data[8]==27:  #confere o byte de checksum
                    parseStatus = True
                else:
                    parseStatus = False
                #proxima execução
                prevmillis2 = currentmillis2

        except Exception as err:
            print(str(err))
            parseStatus = False

        else:
            '''
            aqui deve-se processar os dados e enviar os comandos caso esteja em 
            modo automatico
            '''
            pass
        finally:
            currentmillis = millis()
            if(currentmillis - prevmillis > sendDBinterval):
                #envia dado para o banco de dados (somente se o parse foi feito com sucesso)
                if parseStatus == True:
                    reg = Registers()
                    reg.Temp1 = data[0]
                    reg.Temp2 = data[1]
                    reg.Temp3 = data[2]
                    reg.Temp4 = data[3]    
                    reg.HotFlow = data[4]
                    reg.ColdFlow = data[5]
                    reg.PumpSpeed = data[6]
                    reg.PumpStatus = getbit(data[7],0)
                    reg.HeaterStatus = getbit(data[7],1)
                    reg.TimeStamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
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

    p1 = Process(target=asyncore.loop)
    p1.start()
    p2 = Process(target=mainloop,args=(prevmillis,prevmillis2,))
    p2.start()

    strstatus = 'Servidor rodando'
    print(strstatus)
    


