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



# create a model for the table standard  books with  an id

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.FloatField()
    isbn = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    pubdate = models.DateField()
    comment = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    description2 = models.CharField(max_length=200)
    description3 = models.CharField(max_length=200)
    description4 = models.CharField(max_length=200)
    description5 = models.CharField(max_length=200)
    description6 = models.CharField(max_length=200)
    description7 = models.CharField(max_length=200)
    description8 = models.CharField(max_length=200)
    description9 = models.CharField(max_length=200)


# create a model for the table standard  books with  an id and a foreignkey 

class Book2(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.FloatField()
    isbn = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    pubdate = models.DateField()
    comment = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    description2 = models.CharField(max_length=200)
    description3 = models.CharField(max_length=200)
    description4 = models.CharField(max_length=200)
    description5 = models.CharField(max_length=200)
    description6 = models.CharField(max_length=200)
    description7 = models.CharField(max_length=200)
    description8 = models.CharField(max_length=200)
    description9 = models.CharField(max_length=200)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)       
