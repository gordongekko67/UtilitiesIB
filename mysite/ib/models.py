# Create your models here.
from django.db import models


class Trade(models.Model):
    id = models.AutoField(primary_key=True)
    operazione = models.CharField(max_length=5)
    num_contratti = models.IntegerField()
    descrizione = models.CharField(max_length=200)
    prezzo = models.FloatField()
    valuta = models.CharField(max_length=3)
    data_ora = models.DateTimeField()
    commissione = models.FloatField()
    profitto_perdita = models.FloatField(max_length=100, null=True, blank=True)
    commento = models.CharField(max_length=200)
    descrizione12= models.CharField(max_length=12)

class Trade2(models.Model):
    id2 = models.AutoField(primary_key=True)
    operazione = models.CharField(max_length=5)
    num_contratti = models.IntegerField()
    descrizione = models.CharField(max_length=200)
    prezzo = models.FloatField()
    valuta = models.CharField(max_length=3)
    data_ora = models.DateTimeField()
    commissione = models.FloatField()
    profitto_perdita = models.FloatField(max_length=100, null=True, blank=True)
    commento = models.CharField(max_length=200)
    descrizione12= models.CharField(max_length=12)