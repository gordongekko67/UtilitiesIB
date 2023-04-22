from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
import pandas as pd
from django.http import HttpResponse

def index(request):
     return render(request, "analisi_portafoglio/index.html")


def analisi(request):
    # inporto df 
    template = loader.get_template('analisi_portafoglio/index.html')
    df = pd.read_csv('portfolio.csv')
    df2 = pd.DataFrame()
    print(df2)
    return HttpResponse(template.render())
    


