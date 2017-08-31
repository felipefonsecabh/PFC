from django.db import models

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

