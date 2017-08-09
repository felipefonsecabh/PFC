from django.db import models

# Create your models here.

class DataDisplay(models.Model):
    name = models.CharField('Nome',max_length=20)
    UE = models.TextField('UE',max_length=10,blank=True,null=True)
    description = models.TextField('Descrição Simples',blank=True,null=True)
    Tag = models.TextField('Tag',max_length=10,blank=True,null=True)
    Value = models.FloatField('Valor')

    class Meta:
        verbose_name = 'Display'
        verbose_name_plural = "Displays"
        ordering =['name']

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

