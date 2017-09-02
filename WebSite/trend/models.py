from django.db import models
import time

# Create your models here.
class TrendRegister(models.Model):
    TimeStamp = models.DateTimeField()
    Temp1 = models.FloatField()
    Temp2 = models.FloatField()
    Temp3 = models.FloatField()
    Temp4 = models.FloatField()
    HotFlow = models.FloatField()
    ColdFlow = models.FloatField()
    PumpSpeed = models.FloatField()

    class Meta:
        verbose_name='TrendRegister'
        verbose_name_plural = 'TrendRegisters'
        ordering =['TimeStamp']
    
    def serialize(self):
        data = {}

        data['TimeStamp'] = self.TimeStamp.timestamp()
        data['StrTs'] = self.TimeStamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        data['Temp1'] = self.Temp1
        data['Temp2'] = self.Temp2
        data['Temp3'] = self.Temp3
        data['Temp4']= self.Temp4
        data['ColdFlow']  = self.ColdFlow
        data['HotFlow'] = self.HotFlow
        data['PumpSpeed'] = self.PumpSpeed
        return(data)


