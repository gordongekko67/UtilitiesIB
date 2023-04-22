
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect  
import pandas as pd
import os, re 
import datetime
from .models import Trade2
import yfinance as yf

def index(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())

def index2(request):
  template = loader.get_template('index2.html')
  return HttpResponse(template.render())


def analisi_trades(request):
    template = loader.get_template('index2.html')
    df = pd.read_csv('trade01012023-19042023.csvtrades.csv')
    #eseguo la selezione
    df1 = df.loc[(df['Deltaabs'] > 0.499999) & (df['Posizione'] < 0)]







def importa(request):
    template = loader.get_template('index2.html')
    df = pd.read_csv('trades.csv')
       
    for   i in df.index:
          num_contratti8 = df['Quantity'][i].astype(int)
          prezzo8 = df['Price'][i].astype(float)
          commissione8 = df['Commission'][i].astype(float)
          profitto_perdita8 = df['Realized P&L'][i].astype(float)
          data8=str(df['Date'][i])
          data9 = data8[0:4] + "-" + data8[4:6]   + "-" + data8[6:8]
          time8=str(df['Time'][i])
          datetime8 = data9+" " +time8
          descrizione_ridotta =(df['Fin Instrument'][i])[0:13]
          # scrittura del file 
          q = Trade2(operazione=df['Action'][i], num_contratti=num_contratti8, descrizione =df['Fin Instrument'][i], descrizione12 =descrizione_ridotta,  prezzo=prezzo8, valuta =df['Currency'][i], data_ora=datetime8, commissione =commissione8, profitto_perdita=profitto_perdita8,  commento ="")
          q.save()
                                                                                                                            
    
    return HttpResponse(template.render())


def show(request):  
    #data = myform.cleaned_data
    #field = data['field']

    trades = Trade2.objects.all().filter(descrizione12__startswith="NVS")  
    return render(request,"index3.html",{'trades':trades})  


def importa_portfolio_ITM(request):
    template = loader.get_template('index4.html')
    # inporto df 
    df = pd.read_csv('portfolio.csv')

    # aggiustamenti colonne e dati
    df.rename(columns = {"Strumento finanziario":"Strumento_finanziario", "Giorni restanti all'UGT":"Giorni_rimanenti"}, inplace = True)
    print(df)
    df['Delta'] = df['Delta'].astype(float)
    df['Giorni_rimanenti'] = df['Giorni_rimanenti'].astype(int)

    df["Deltaabs"] = abs(df['Delta'].astype(float))
    
    #eseguo la selezione
    df1 = df.loc[(df['Deltaabs'] > 0.499999) & (df['Posizione'] < 0)]
    
    #li ordino 
    df4 = df1.sort_values(['Giorni_rimanenti','Deltaabs','Strumento_finanziario'],
              ascending = [True, False, True])

             

    #emissione videata
    trades = df4
    return render(request,"index4.html",{'trades':trades})  












def importa_portfolio_con_rischio_di_assegnazione(request):
    template = loader.get_template('index5.html')
    # inporto df 
    df = pd.read_csv('portfolio.csv')
    df2 = pd.DataFrame()
    

    # aggiustamenti colonne e dati
    df.rename(columns = {"Strumento finanziario":"Strumento_finanziario", "Giorni restanti all'UGT":"Giorni_rimanenti"}, inplace = True)
    df['Delta'] = df['Delta'].astype(float)
    df['Giorni_rimanenti'] = df['Giorni_rimanenti'].astype(int)

    df["Deltaabs"] = abs(df['Delta'].astype(float))
    
    df["Valore temporale (%)"].replace("", 99.999, inplace=True)
    
    df["Valore_tmp_fin"] = df["Valore temporale (%)"].str.extract(r"(\d+\.\d+)")
    df["Valore_tmp_fin_float"] = df["Valore_tmp_fin"].astype(float)
   
    df2 = df.loc[(df['Deltaabs'] > 0.499) & (df['Valore_tmp_fin_float'] < 0.5)]
 

   
         
    #emissione videata
    trades = df2
    print(trades)
    return render(request,"index5.html",{'trades':trades})  



def importa_portfolio_da_rollare_profitto(request):
    template = loader.get_template('index4.html')
    # inporto df 
    df = pd.read_csv('portfolio.csv')

    # aggiustamenti colonne e dati
    df.rename(columns = {"Strumento finanziario":"Strumento_finanziario", "Giorni restanti all'UGT":"Giorni_rimanenti"}, inplace = True)
    print(df)
    df['Delta'] = df['Delta'].astype(float)
    df['Giorni_rimanenti'] = df['Giorni_rimanenti'].astype(int)

    df["Deltaabs"] = abs(df['Delta'].astype(float))
    df["Posizione"] = df['Posizione'].astype(int)
    #eseguo la selezione
    df1 = df.loc[(df['Deltaabs'] < 0.075) & (df['Posizione'] < 0)]
   
    #li ordino 
    df4= df1.sort_values(by=['Deltaabs'],  ascending=False)
    
         
    #emissione videata
    trades = df4
    return render(request,"index4.html",{'trades':trades})  


def importa_trades(request):
    
    df = pd.read_csv('Analisi_trade.csv')
    df1 = df.loc[(df['Realizzato Perdita S/T'] < -999)]
    df2 = df1.drop(["Sommario profitti e perdite Realizzati e Non realizzati", "Header"], axis=1)
    print(df2)
    df2.to_csv("analisi_perdite.csv", index = False)

    #emissione videata
    trades = df2
    return render(request,"index4.html",{'trades':trades}) 




def analisi_trade_scadenza(request):
    df = pd.read_csv('Analisi_trade.csv')
    df2 = df.drop(["Sommario profitti e perdite Realizzati e Non realizzati", "Header"], axis=1)
      
    df2['Simbolo_solo'] = df['Simbolo'].str.split(' ').str[0]
    df2['Simbolo_opzione'] = df['Simbolo'].str.split(' ').str[0] + df['Simbolo'].str.split(' ').str[1] 
    df2.sort_values(by=['Simbolo_opzione'], inplace = True)
          
    # raggruppa il dataframe per il campo "campo1" e somma i valori per ogni gruppo
    df_grouped = df2.groupby('Simbolo_opzione')['Realizzato Totale', 'Non realizzato Totale','Totale'].sum().reset_index()
    
    #emissione videata
    trades = df_grouped
    return render(request,"index4.html",{'trades':trades}) 


def analisi_trade_titolo(request):
    df = pd.read_csv('Analisi_trade.csv')
    df2 = df.drop(["Sommario profitti e perdite Realizzati e Non realizzati", "Header"], axis=1)
      
    df2['Simbolo_solo'] = df['Simbolo'].str.split(' ').str[0]
    df2['Simbolo_opzione'] = df['Simbolo'].str.split(' ').str[0] + df['Simbolo'].str.split(' ').str[1] 
    df2.sort_values(by=['Simbolo_opzione'], inplace = True)
          
    # raggruppa il dataframe per il campo "campo1" e somma i valori per ogni gruppo
    df_grouped = df2.groupby('Simbolo_solo')['Realizzato Totale', 'Non realizzato Totale','Totale'].sum().reset_index()
    #emissione videata
    trades = df_grouped
    return render(request,"index4.html",{'trades':trades}) 


def analisi_trade_dettaglio(request):
    df = pd.read_csv('Analisi_trade.csv')
    df2 = df.drop(["Sommario profitti e perdite Realizzati e Non realizzati", "Header"], axis=1)
      
    df2['Simbolo_solo'] = df['Simbolo'].str.split(' ').str[0]
    df2['Simbolo_opzione'] = df['Simbolo'].str.split(' ').str[0] + df['Simbolo'].str.split(' ').str[1] 
    df2.sort_values(by=['Simbolo_opzione'], inplace = True)
          
        #emissione videata
    trades = df2
    return render(request,"index4.html",{'trades':trades}) 















def analisi_bilanciamento_delta(request):
    template = loader.get_template('index4.html')
    # inporto df 
    df = pd.read_csv('portfolio.csv')

    # aggiustamenti colonne e dati
    df.rename(columns = {"Strumento finanziario":"Strumento_finanziario", "Giorni restanti all'UGT":"Giorni_rimanenti"}, inplace = True)
    print(df)
    df['Delta'] = df['Delta'].astype(float)
    df['Deltasigned'] = df['Delta'].astype(float)
    df['Giorni_rimanenti'] = df['Giorni_rimanenti'].astype(int)

    df["Deltaabs"] = abs(df['Delta'].astype(float))
    df["Posizione"] = df['Posizione'].astype(int)
    df['Simbolo_solo'] = df['Strumento_finanziario'].str.split(' ').str[0]
    #eseguo la selezione
    df1 = df.loc[(df['Deltaabs'] < 0.075) & (df['Posizione'] < 0)]
    df["Deltariga"] = df["Delta"]*df['Posizione']*100
    
    #li ordino 
    df4= df.sort_values(by=['Deltaabs'],  ascending=False)
    # raggruppa il dataframe per il campo "campo1" e somma i valori per ogni gruppo
    df_grouped = df4.groupby('Simbolo_solo')['Deltariga'].sum().reset_index()

    # seleziona solo le righe con valori maggiori di 50 in 'Deltariga'
    df_grouped.sort_values(by=['Deltariga'], inplace = True, ascending=False)
      
    #emissione videata
    trades = df_grouped
    return render(request,"index4.html",{'trades':trades})  






def opzioni_PUT_da_rollare(request):
    template = loader.get_template('index5.html')
    # inporto df 
    df = pd.read_csv('portfolio.csv')
    df2 = pd.DataFrame()
    

    # aggiustamenti colonne e dati
    df.rename(columns = {"Strumento finanziario":"Strumento_finanziario", "Giorni restanti all'UGT":"Giorni_rimanenti"}, inplace = True)
    df['Delta'] = df['Delta'].astype(float)
    df['Giorni_rimanenti'] = df['Giorni_rimanenti'].astype(int)

    df["Deltaabs"] = abs(df['Delta'].astype(float))
    
    df["Valore temporale (%)"].replace("", 99.999, inplace=True)
    
    df["Valore_tmp_fin"] = df["Valore temporale (%)"].str.extract(r"(\d+\.\d+)")
    df["Valore_tmp_fin_float"] = df["Valore_tmp_fin"].astype(float)
    df['PUT/CALL'] = df['Strumento_finanziario'].str.split(' ').str[3]
   
    df2 = df.loc[(df['Giorni_rimanenti'] < 21) & (df['Deltaabs'] > 0.5) & (df['PUT/CALL'] =="PUT")]
 
    trades = df2
    return render(request,"index4.html",{'trades':trades})  


def opzioni_CALL_da_vedere_se_andare_invertito(request):
    template = loader.get_template('index5.html')
    # inporto df 
    df = pd.read_csv('portfolio.csv')
    df2 = pd.DataFrame()
    

    # aggiustamenti colonne e dati
    df.rename(columns = {"Strumento finanziario":"Strumento_finanziario", "Giorni restanti all'UGT":"Giorni_rimanenti"}, inplace = True)
    df['Delta'] = df['Delta'].astype(float)
    df['Giorni_rimanenti'] = df['Giorni_rimanenti'].astype(int)

    df["Deltaabs"] = abs(df['Delta'].astype(float))
    
    df["Valore temporale (%)"].replace("", 99.999, inplace=True)
    
    df["Valore_tmp_fin"] = df["Valore temporale (%)"].str.extract(r"(\d+\.\d+)")
    df["Valore_tmp_fin_float"] = df["Valore_tmp_fin"].astype(float)
    df['PUT/CALL'] = df['Strumento_finanziario'].str.split(' ').str[3]
   
    df2 = df.loc[(df['Giorni_rimanenti'] < 21) & (df['Deltaabs'] > 0.5) & (df['PUT/CALL'] =="CALL")]
 
    trades = df2
    return render(request,"index4.html",{'trades':trades})  



def analisi_di_portafoglio(request):
    template = loader.get_template('index4.html')
    # inporto df 
    df = pd.read_csv('portfolio.csv')
    # aggiustamenti colonne e dati
    df.rename(columns = {"Strumento finanziario":"Strumento_finanziario", "Giorni restanti all'UGT":"Giorni_rimanenti"}, inplace = True)

    df['Delta'] = df['Delta'].astype(float)
    df['Giorni_rimanenti'] = df['Giorni_rimanenti'].astype(int)

    df["Deltaabs"] = abs(df['Delta'].astype(float))
    
    df["Valore temporale (%)"].replace("", 99.999, inplace=True)
    
    df["Val_tmp_fin"] = df["Valore temporale (%)"].str.extract(r"(\d+\.\d+)")
    df["Val_tmp_fin_float"] = df["Val_tmp_fin"].astype(float)
    df['PUT/CALL'] = df['Strumento_finanziario'].str.split(' ').str[3]
    df['Simbolo_solo'] = df['Strumento_finanziario'].str.split(' ').str[0]
    df.drop(['Operazione ticker'], axis = 1) 

   
    df2 = df.loc[(df['Giorni_rimanenti'] < 30) & (df['Deltaabs'] > 0.5) ]
    df3 = df.loc[(df['Val_tmp_fin_float'] < 1.5 ) & (df['Deltaabs'] > 0.5)]
    
    df4= pd.concat([df2, df3])
    
    # lettura df
    for i in df4.index: 
       stock = yf.Ticker(df4['Simbolo_solo'][i])
       price = stock.info['currentPrice']
       df4['current_price'] = price
       print(df4)

       



    trades = df4
    return render(request,"index4.html",{'trades':trades})  

