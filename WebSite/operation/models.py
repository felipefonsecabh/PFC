from django.db import models

# Create your models here.

class DataDisplay(models.Model):
    name = models.CharField('Nome',max_length=20)
    UE = models.CharField('UE',max_length=10,blank=True,null=True)
    description = models.TextField('Descrição Simples',blank=True,null=True)
    Tag = models.CharField('Tag',max_length=10,blank=True,null=True)
    Value = models.FloatField('Valor')

    class Meta:
        verbose_name = 'Display'
        verbose_name_plural = "Displays"
        ordering =['name']

    def __str__(self):
        return self.name


class Registers(models.Model):
    TimeStamp = models.DateTimeField()
    Temp1 = models.FloatField()
    Temp2 = models.FloatField()
    Temp3 = models.FloatField()
    Temp4 = models.FloatField()
    HotFlow = models.FloatField()
    ColdFlow = models.FloatField()
    PumpStatus = models.BooleanField()
    HeaterStatus = models.BooleanField()
    PumpSpeed = models.FloatField()

    class Meta:
        verbose_name='Register'
        verbose_name_plural = 'Registers'
        ordering =['TimeStamp']

    def getintspeed(self):
        return int(self.PumpSpeed)

