from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import pandas as pd


def index(request):
  
    return render(request, "analisi_portafoglio/index.html")


def analisi(request):
    # inporto df 
    df = pd.read_csv('portfolio.csv')
    df2 = pd.DataFrame()
    print(df2)



