
# Create your views here.
from django.http import HttpResponse
from django.template import loader, Template, Context
from django.shortcuts import render, redirect
import pandas as pd
import os
import re
import datetime
from .models import Trade2
import yfinance as yf
import traceback
import sys
import matplotlib.pyplot as plt
import numpy as np


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def index2(request):
    template = loader.get_template('index2.html')
    return HttpResponse(template.render())


def analisi_trades(request):
    template = loader.get_template('index2.html')
    df = pd.read_csv('trade01012023-19042023.csvtrades.csv')
    # eseguo la selezione
    df1 = df.loc[(df['Deltaabs'] > 0.499999) & (df['Posizione'] < 0)]


def importa(request):
    template = loader.get_template('index2.html')
    df = pd.read_csv('trades.csv')

    for i in df.index:
        num_contratti8 = df['Quantity'][i].astype(int)
        prezzo8 = df['Price'][i].astype(float)
        commissione8 = df['Commission'][i].astype(float)
        profitto_perdita8 = df['Realized P&L'][i].astype(float)
        data8 = str(df['Date'][i])
        data9 = data8[0:4] + "-" + data8[4:6] + "-" + data8[6:8]
        time8 = str(df['Time'][i])
        datetime8 = data9+" " + time8
        descrizione_ridotta = (df['Fin Instrument'][i])[0:13]
        # scrittura del file
        q = Trade2(operazione=df['Action'][i], num_contratti=num_contratti8, descrizione=df['Fin Instrument'][i], descrizione12=descrizione_ridotta,
                   prezzo=prezzo8, valuta=df['Currency'][i], data_ora=datetime8, commissione=commissione8, profitto_perdita=profitto_perdita8,  commento="")
        q.save()

    return HttpResponse(template.render())


def show(request):
    # data = myform.cleaned_data
    # field = data['field']

    trades = Trade2.objects.all().filter(descrizione12__startswith="NVS")
    return render(request, "index3.html", {'trades': trades})


def importa_portfolio_ITM(request):
    template = loader.get_template('index4.html')
    # inporto df
    df = pd.read_csv('portfolio.csv')

    # aggiustamenti colonne e dati
    df.rename(columns={"Strumento finanziario": "Strumento_finanziario",
              "Giorni restanti all'UGT": "GG_rim"}, inplace=True)
    print(df)
    df['Delta'] = df['Delta'].astype(float)
    df['GG_rim'] = df['GG_rim'].astype(int)

    df["Deltaabs"] = abs(df['Delta'].astype(float))

    # eseguo la selezione
    df1 = df.loc[(df['Deltaabs'] > 0.499999) & (df['Posizione'] < 0)]

    # li ordino
    df4 = df1.sort_values(['GG_rim', 'Deltaabs', 'Strumento_finanziario'],
                          ascending=[True, False, True])

    # emissione videata
    trades = df4
    return render(request, "index4.html", {'trades': trades})


def importa_portfolio_ITM_valore_temporale(request):
    template = loader.get_template('index4.html')
    # inporto df
    df = pd.read_csv('portfolio.csv')

    # aggiustamenti colonne e dati
    df.rename(columns={"Strumento finanziario": "Strumento_finanziario",
              "Giorni restanti all'UGT": "GG_rim"}, inplace=True)
    print(df)
    df['Delta'] = df['Delta'].astype(float)
    df['GG_rim'] = df['GG_rim'].astype(int)

    df["Deltaabs"] = abs(df['Delta'].astype(float))

    # eseguo la selezione
    df1 = df.loc[(df['Deltaabs'] > 0.499999) & (df['Posizione'] < 0)]

    # estraggo il primo campo del valore temporale e lo converto in float
    df1["Valore temporale (%)"].replace("", 99.999, inplace=True)

    df1["Valore_tmp_fin"] = df1["Valore temporale (%)"].str.extract(
        r"(\d+\.\d+)")
    df1["Valore_tmp_fin_float"] = df1["Valore_tmp_fin"].astype(float)

    # elimino la colonna simbolo_solo e operazione ticker
    df1.drop(["Operazione ticker"], axis=1, inplace=True)

     # se il valore temporale float è maggiore di 4,5 lo elimino
    #df1 = df1[df1['Valore_tmp_fin_float'] < 4.5]
    print(df1)


    # li ordino
    df4 = df1.sort_values(['Valore_tmp_fin_float'],
                          ascending=[True])

    # emissione videata
    trades = df4
    return render(request, "index4.html", {'trades': trades})

def importa_portfolio_ITM_valore_temporale_percentuale(request):
    template = loader.get_template('index4.html')
    # inporto df
    df = pd.read_csv('portfolio.csv')

    # aggiustamenti colonne e dati
    df.rename(columns={"Strumento finanziario": "Strumento_finanziario",
              "Giorni restanti all'UGT": "GG_rim"}, inplace=True)
    print(df)
    df['Delta'] = df['Delta'].astype(float)
    df['GG_rim'] = df['GG_rim'].astype(int)

    df["Deltaabs"] = abs(df['Delta'].astype(float))

    # eseguo la selezione
    df1 = df.loc[(df['Deltaabs'] > 0.499999) & (df['Posizione'] < 0)]

    stringa = str(df1["Valore temporale (%)"].str.extract(
        r"\((\d+\.\d+)\)"))
    
   

    df1["Valore_tmp_perc"] = df1["Valore temporale (%)"].str.extract(
        r"\((\d+\.\d+)\)")
    df1["Valore_tmp_perc_float"] = df1["Valore_tmp_perc"].astype(float)

    print(df1)

    # faccio un ciclo di lettura sul df1
    for i in df1.index:
        # se df1['Strumento_finanziario'][i] non comincia con QQQ

        if not df1['Strumento_finanziario'][i].startswith('QQQ'):
       
            print(df1['Strumento_finanziario'][i])
            # con simbolo solo vado a predenermi il ticker su yahoo finance
            simbolo_solo = df1['Strumento_finanziario'][i].split(' ')[0]
            # vado a prednere il prezzo su yahho  finance
            ticker = yf.Ticker(simbolo_solo)
            # prendo il prezzo
            prezzo = ticker.info['currentPrice']
       
            # prendo il valore temporale come primo campo di valore temporale % e lo converto in float
            valore_temporale = df1['Valore temporale (%)'][i].split(' ')[0]
            valore_temporale = float(valore_temporale)

            # vado a prendere il vaore dello strike e lo converto in float
            strike = df1['Strumento_finanziario'][i].split(' ')[2]
            strike_float = float(strike)
            # faccio la diferenza  tra prezzo e strike in valore assoluto
            differenza = abs(prezzo - strike_float)

       
            # se in df['Ultimo'] ho una stringa che comincia con 'c'
            # elimino la c e converto in float
            if df1['Ultimo'][i].startswith('C'):
               df1['Ultimo'][i] = df1['Ultimo'][i].replace('C', '')
               df1['Ultimo'][i] = float(df1['Ultimo'][i])
               print("ho trovato una c")
               print(df1['Ultimo'][i])
        

            # reperisco il prezzo medio pagato e lo converto in float
            prezzo_ultimo = df1['Ultimo'][i]
            print(df1['Ultimo'][i], df1['Strumento_finanziario'][i])
            prezzo_ultimo = float(prezzo_ultimo)

            # calcolo la percentuale come valore temporale/prezzo medio e arrotiondo a 2 decimali
            percentuale = round((valore_temporale/prezzo_ultimo)*100, 2)
                    

            print(simbolo_solo, prezzo_ultimo, strike,   valore_temporale, differenza, percentuale)
            # adesso devo aggiungere la precentuale alla riga i del mio df1
            df1['Valore_tmp_perc'][i] = percentuale
            df1['Valore_tmp_perc_float'][i] = valore_temporale

        


    # copia la colonna Valore_tmp_perc in prima posizione nel dataframe 
    df1.insert(2, "Valore_temporale espresso in %   ", df1['Valore_tmp_perc'], True)
    df1.insert(3, "Valore_temporale espresso in valore assoluto  ", df1['Valore_tmp_perc_float'], True)


    # elimino la colonna Modifica
    df1.drop(["Modifica"], axis=1, inplace=True)
    # elimino la colonna Variazione % e Deltaabs
    df1.drop(["Variazione %", "Deltaabs"], axis=1, inplace=True)
    
        
    

    # ordino il data_frame per Valore_tmp_perc

    df4 = df1.sort_values(['Valore_tmp_perc'],
                            ascending=[True])
    
    # elimino la colonna Valore_tmp_perc_float, e Valore_tmp_perc
    df4.drop(["Valore_tmp_perc_float", "Valore_tmp_perc"], axis=1, inplace=True)
    
    

    # emissione videata
    trades = df4
    return render(request, "index4.html", {'trades': trades})
 


    



def importa_portfolio_con_rischio_di_assegnazione(request):
    template = loader.get_template('index5.html')
    # inporto df
    df = pd.read_csv('portfolio.csv')
    df2 = pd.DataFrame()

    # aggiustamenti colonne e dati
    df.rename(columns={"Strumento finanziario": "Strumento_finanziario",
              "Giorni restanti all'UGT": "GG"}, inplace=True)
    df['Delta'] = df['Delta'].astype(float)
    df['GG'] = df['GG'].astype(int)

    df["Deltaabs"] = abs(df['Delta'].astype(float))

    df["Valore temporale (%)"].replace("", 99.999, inplace=True)

    df["Valore_tmp_fin"] = df["Valore temporale (%)"].str.extract(
        r"(\d+\.\d+)")
    df["Valore_tmp_fin_float"] = df["Valore_tmp_fin"].astype(float)

    df2 = df.loc[(df['Deltaabs'] > 0.499) & (df['Valore_tmp_fin_float'] < 2.5)]

    # li ordino per valore temporale crescente
    df4 = df2.sort_values(['Valore_tmp_fin_float'],
                            ascending=[True])
    

    # emissione videata
    trades = df4
    print(trades)
    return render(request, "index5.html", {'trades': trades})


def importa_portfolio_da_rollare_profitto(request):
    template = loader.get_template('index4.html')
    # inporto df
    df = pd.read_csv('portfolio.csv')

    # aggiustamenti colonne e dati
    df.rename(columns={"Strumento finanziario": "Strumento_finanziario",
              "Giorni restanti all'UGT": "Giorni_rimanenti"}, inplace=True)
    print(df)
    df['Delta'] = df['Delta'].astype(float)
    df['Giorni_rimanenti'] = df['Giorni_rimanenti'].astype(int)

    df["Deltaabs"] = abs(df['Delta'].astype(float))
    df["Posizione"] = df['Posizione'].astype(int)
    # eseguo la selezione
    df1 = df.loc[(df['Deltaabs'] < 0.075) & (df['Posizione'] < 0)]

    # li ordino
    df4 = df1.sort_values(by=['Deltaabs'],  ascending=False)

    # emissione videata
    trades = df4
    return render(request, "index4.html", {'trades': trades})


def importa_trades(request):

    df = pd.read_csv('Analisi_trade.csv')
    df1 = df.loc[(df['Realizzato Perdita S/T'] < -999)]
    df2 = df1.drop(
        ["Sommario profitti e perdite Realizzati e Non realizzati", "Header"], axis=1)
    print(df2)
    df2.to_csv("analisi_perdite.csv", index=False)

    # emissione videata
    trades = df2
    return render(request, "index4.html", {'trades': trades})


def analisi_trade_scadenza(request):
    df = pd.read_csv('Analisi_trade.csv')
    df2 = df.drop(
        ["Sommario profitti e perdite Realizzati e Non realizzati", "Header"], axis=1)

    df2['Simbolo_solo'] = df['Simbolo'].str.split(' ').str[0]
    df2['Simbolo_opzione'] = df['Simbolo'].str.split(
        ' ').str[0] + df['Simbolo'].str.split(' ').str[1]
    df2.sort_values(by=['Simbolo_opzione'], inplace=True)

    print(df2)

    # prendo il quarto elemento di Simbolo che sarebbe se CALL o PUT
    df2['Tipo_CALL_PUT'] = df['Simbolo'].str.split(' ').str[3]    

    print(df2)

    # prendo solo le righe con Tipo_CALL_PUT = 'C'
    df2 = df2[df2['Tipo_CALL_PUT'] == 'P']


    # raggruppa il dataframe per il campo "Simbolo_opzione" e somma i valori per ogni gruppo
    df_grouped = df2.groupby('Simbolo_opzione').agg(
        {'Realizzato Totale': 'sum', 'Non realizzato Totale': 'sum', 'Totale': 'sum'}).reset_index()

    trades0 = df_grouped[['Simbolo_opzione',
                          'Realizzato Totale', 'Non realizzato Totale', 'Totale']]
    trades = trades0.sort_values(by=['Totale'],  ascending=True)

    # vorrei solo aggiungere un contatopre di riga a trades per poterlo usare in html come indice sequenziale
    # per vedere quante righe ho in totale
    trades['contatore'] = range(1, len(trades) + 1)
    # perfetto solo il valore dovrebbe essere allineato a destra
    trades['contatore'] = trades['contatore'].astype(str).str.rjust(3, '0')

     # faccio una somma finale per avere il totale del realizzato e non realizzato Totale
    trades.loc['Totale'] = trades.sum(numeric_only=True, axis=0)

    # copio il datframe in un altro per poterlo modificare con solo totale
    trades2 = trades.copy()
    # lascio solo la colonna totale
    trades2 = trades2[['Simbolo_opzione', 'Totale']]
    
    # lo trasformo in numeri con due decimali per la visulaizzazione solo 
    trades2['Totale'] = trades2['Totale'].round(2)
    # lo visualizzo con matplotlib
    trades2.plot.bar(x='Simbolo_opzione', y=['Totale'], rot=0, figsize=(15, 10))
    # faccio un diagramma a punti
    #trades2.plot(x='Simbolo_opzione', y=['Totale'], kind='scatter', figsize=(15, 10))


    print(trades2)

    # visualizzo trade2
    plt.show()
    
    # salvo il grafico
    plt.savefig('scadenza.png')
   
       

    # emissione videata
    return render(request, "index4.html", {'trades': trades})


def analisi_trade_scadenza_simbolo(request):
    df = pd.read_csv('Analisi_trade.csv')
    df2 = df.drop(
        ["Sommario profitti e perdite Realizzati e Non realizzati", "Header"], axis=1)

    df2['Simbolo_solo'] = df['Simbolo'].str.split(' ').str[0]
    df2['Simbolo_opzione'] = df['Simbolo'].str.split(
        ' ').str[0] + df['Simbolo'].str.split(' ').str[1]
    df2.sort_values(by=['Simbolo_opzione'], inplace=True)

    # raggruppa il dataframe per il campo "Simbolo_opzione" e somma i valori per ogni gruppo
    df_grouped = df2.groupby('Simbolo_opzione').agg(
        {'Realizzato Totale': 'sum', 'Non realizzato Totale': 'sum', 'Totale': 'sum'}).reset_index()

    trades0 = df_grouped[['Simbolo_opzione',
                          'Realizzato Totale', 'Non realizzato Totale', 'Totale']]
    trades = trades0.sort_values(by=['Simbolo_opzione'],  ascending=True)

    # faccio un totale finale
    trades.loc['Totale'] = trades.sum(numeric_only=True, axis=0)

    # emissione videata
    return render(request, "index4.html", {'trades': trades})


def analisi_trade_scadenza_simbolo_2(request):
    df = pd.read_csv('Analisi_trade.csv')
    df2 = df.drop(
        ["Sommario profitti e perdite Realizzati e Non realizzati", "Header"], axis=1)

    df2['Simbolo_solo'] = df['Simbolo'].str.split(' ').str[0]
    df2['Data_scadenza'] = df['Simbolo'].str.split(' ').str[1]
    df2['Simbolo_opzione'] = df['Simbolo'].str.split(
        ' ').str[0] + df['Simbolo'].str.split(' ').str[1]
    

    # estraggo quelli che in simbolo_solo_mese = a 21JUL23
    #df2 = df2[df2['Data_scadenza'] == '21JUL23']
        
    # vorrei raggruppare df2 per data_scadenza e simbolo_solo e poi sommare i valori di realizzato totale e non realizzato totale
    # e poi ordinare per data_scadenza e simbolo_solo crescente e fare i totali per ogni data_scadenza
    # e poi un totale finale
        
    df2.sort_values(by=['Data_scadenza', 'Simbolo_solo'], inplace=True)
    # raggruppa il dataframe per il campo "Data_scadenza" e "Simbolo_solo" e somma i valori per ogni gruppo
    df_grouped = df2.groupby(['Data_scadenza', 'Simbolo_solo']).agg(
        {'Realizzato Totale': 'sum', 'Non realizzato Totale': 'sum', 'Totale': 'sum'}).reset_index()
    # ogni volta che cambia la data_scadenza devo fare un totale
    trades0 = df_grouped[['Data_scadenza', 'Simbolo_solo', 'Realizzato Totale', 'Non realizzato Totale', 'Totale']]
    #trades.loc['Totale_data'] = trades0.sum(numeric_only=True, axis=0)

    # faccio un totlae a cambio di data scadenza
    trades0.loc['Totale_data'] = trades0.sum(numeric_only=True, axis=0)
    

    # faccio un totale finale di tutto
    trades = trades0.sort_values(by=['Data_scadenza', 'Simbolo_solo'],  ascending=True)
    trades.loc['Totale'] = trades.sum(numeric_only=True, axis=0)
         
        
    # emissione videata
    return render(request, "index4.html", {'trades': trades})



def analisi_trade_scadenza_simbolo_3(request):
    df = pd.read_csv('Analisi_trade.csv')
    df2 = df.drop(
        ["Sommario profitti e perdite Realizzati e Non realizzati", "Header"], axis=1)

    df2['Simbolo_solo'] = df['Simbolo'].str.split(' ').str[0]
    df2['Data_scadenza'] = df['Simbolo'].str.split(' ').str[1]
    df2['Simbolo_opzione'] = df['Simbolo'].str.split(
        ' ').str[0] + df['Simbolo'].str.split(' ').str[1]
    

    print(df2)
        
    # estraggo da data scadenza solo il mese cge sarebbe solo il terzo quarto quinto carattere 
    df2['Data_scadenza_mese'] = df2['Data_scadenza'].str[2:5]

    # associao a data_scadenza_mese un numero
    df2['Data_scadenza_mese_numero'] = df2['Data_scadenza_mese'].replace(['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG',
                                                                     'SEP', 'OCT', 'NOV', 'DEC'], ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                                                                                     
                                                                                                    '11', '12'])
    
    # estraggo da data scadenza solo l'anno che sarebbe solo il sesto e settimo carattere
    df2['Data_scadenza_anno'] = df2['Data_scadenza'].str[6:7]
    
    # aggiungo un campo con datascadenza_anno + datascadenza_mese
    df2['Data_scadenza_mese_anno'] = df2['Data_scadenza_anno'] + df2['Data_scadenza_mese_numero']

    # adesso ordino per data_scadenza_mese_anno e simbolo_solo

    df2.sort_values(by=['Data_scadenza_mese_anno', 'Simbolo_solo'], inplace=True)

    # raggruppa il dataframe per il campo "Data_scadenza_mese_anno" e "Simbolo_solo" e somma i valori per ogni gruppo
    # a cambiamento di data_scadenza_mese_anno devo fare un totale
    df_grouped = df2.groupby(['Data_scadenza_mese_anno']).agg(
        {'Realizzato Totale': 'sum', 'Non realizzato Totale': 'sum', 'Totale': 'sum'}).reset_index()
    
    trades = df_grouped[['Data_scadenza_mese_anno', 'Realizzato Totale', 'Non realizzato Totale', 'Totale']]

    # faccio un totale finale di tutto
    trades.loc['Totale'] = trades.sum(numeric_only=True, axis=0)         
        
    # emissione videata
    return render(request, "index4.html", {'trades': trades})











def analisi_trade_scadenza_simbolo_ancora_aperte(request):
    df = pd.read_csv('Analisi_trade.csv')
    df2 = df.drop(
        ["Sommario profitti e perdite Realizzati e Non realizzati", "Header"], axis=1)

    df2['Simbolo_solo'] = df['Simbolo'].str.split(' ').str[0]
    df2['Simbolo_opzione'] = df['Simbolo'].str.split(
        ' ').str[0] + df['Simbolo'].str.split(' ').str[1]
    df2.sort_values(by=['Simbolo_opzione'], inplace=True)

    # raggruppa il dataframe per il campo "Simbolo_opzione" e somma i valori per ogni gruppo
    df_grouped = df2.groupby('Simbolo_opzione').agg(
        {'Realizzato Totale': 'sum', 'Non realizzato Totale': 'sum', 'Totale': 'sum'}).reset_index()

    trades0 = df_grouped[['Simbolo_opzione',
                          'Realizzato Totale', 'Non realizzato Totale', 'Totale']]
    trades = trades0.sort_values(by=['Simbolo_opzione'],  ascending=True)

    # devo prendere di trades solo le righe con non realizzato diverso da 0
    trades = trades[trades['Non realizzato Totale'] != 0]

    # li ordino per Simbolo_opzione crescente
    trades = trades.sort_values(by=['Simbolo_opzione'],  ascending=True)

    # faccio una somma finale per avere il totale del realizzato e non realizzato Totale
    trades.loc['Totale'] = trades.sum(numeric_only=True, axis=0)


    # emissione videata
    return render(request, "index4.html", {'trades': trades})





def analisi_trade_scadenza_simbolo_completamente_chiuse(request):
    df = pd.read_csv('Analisi_trade.csv')
    df2 = df.drop(
        ["Sommario profitti e perdite Realizzati e Non realizzati", "Header"], axis=1)

    df2['Simbolo_solo'] = df['Simbolo'].str.split(' ').str[0]
    df2['Simbolo_opzione'] = df['Simbolo'].str.split(
        ' ').str[0] + df['Simbolo'].str.split(' ').str[1]
    df2.sort_values(by=['Simbolo_opzione'], inplace=True)

    # raggruppa il dataframe per il campo "Simbolo_opzione" e somma i valori per ogni gruppo
    df_grouped = df2.groupby('Simbolo_opzione').agg(
        {'Realizzato Totale': 'sum', 'Non realizzato Totale': 'sum', 'Totale': 'sum'}).reset_index()

    trades0 = df_grouped[['Simbolo_opzione',
                          'Realizzato Totale', 'Non realizzato Totale', 'Totale']]
    

    # devo prendere di trades solo le righe con realizzato diverso da 0 e non realizzato uguale a 0
    trades = trades0[trades0['Realizzato Totale'] != 0]
    
    trades = trades.sort_values(by=['Simbolo_opzione'],  ascending=True)

    # faccio una somma finale per avere il totale del realizzato e non realizzato Totale
    trades.loc['Totale'] = trades.sum(numeric_only=True, axis=0)
    
    # emissione videata
    return render(request, "index4.html", {'trades': trades})


def analisi_trade_titolo(request):
    df = pd.read_csv('Analisi_trade.csv')
    df2 = df.drop(
        ["Sommario profitti e perdite Realizzati e Non realizzati", "Header"], axis=1)

    df2['Simbolo_solo'] = df['Simbolo'].str.split(' ').str[0]
    df2.sort_values(by=['Simbolo_solo'], inplace=True)

    # devo eliminare dal dataframe quelli  che hanno simbolo solo = 'USD'
    df2 = df2[df2['Simbolo_solo'] != 'USD']

    # raggruppa il dataframe per il campo "Simbolo_opzione" e somma i valori per ogni gruppo
    df_grouped = df2.groupby('Simbolo_solo').agg(
        {'Realizzato Totale': 'sum', 'Non realizzato Totale': 'sum', 'Totale': 'sum'}).reset_index()

    # trades = df_grouped[['Simbolo_opzione', 'Realizzato Totale', 'Non realizzato Totale', 'Totale']]
    trades0 = df_grouped[[
        'Simbolo_solo', 'Non realizzato Totale', 'Realizzato Totale',  'Totale']]
    trades = trades0.sort_values(by=['Totale'],  ascending=True)


    # faccio una somma finale per avere il totale del realizzato e non realizzato Totale
    trades.loc['Totale'] = trades.sum(numeric_only=True, axis=0)

    # emissione videata
    return render(request, "index4.html", {'trades': trades})


def analisi_trade_dettaglio(request):
    df = pd.read_csv('Analisi_trade.csv')
    df2 = df.drop(
        ["Sommario profitti e perdite Realizzati e Non realizzati", "Header"], axis=1)
    df2 = df.drop(["Realizzato Profitto S/T",
                  "Realizzato Perdita S/T"], axis=1)

    df2['Simbolo_solo'] = df['Simbolo'].str.split(' ').str[0]
    df2['Simbolo_opzione'] = df['Simbolo'].str.split(
        ' ').str[0] + df['Simbolo'].str.split(' ').str[1]
    df2.sort_values(by=['Simbolo_opzione'], inplace=True)

    # emissione videata
    trades = df2
    return render(request, "index4.html", {'trades': trades})


def analisi_trade_dettaglio_simbolo_ancora_aperte(request):
    df = pd.read_csv('Analisi_trade.csv')
    df2 = df.drop(
        ["Sommario profitti e perdite Realizzati e Non realizzati", "Header"], axis=1)
    df2 = df.drop(["Realizzato Profitto S/T",
                  "Realizzato Perdita S/T"], axis=1)

    # voglio includere solo le righe con  non realizzato maggiore di 0
    df2 = df2[df2['Non realizzato Totale'] > 0]

    df2['Simbolo_solo'] = df['Simbolo'].str.split(' ').str[0]
    df2['Simbolo_opzione'] = df['Simbolo'].str.split(
        ' ').str[0] + df['Simbolo'].str.split(' ').str[1]
    df2.sort_values(by=['Simbolo_opzione'], inplace=True)

    # emissione videata
    trades = df2
    return render(request, "index4.html", {'trades': trades})


def analisi_bilanciamento_delta(request):
    fruits = ['Totale Delta Portafoglio  ']
    template = loader.get_template('index4.html')
    # inporto df
    df = pd.read_csv('portfolio.csv')

    # aggiustamenti colonne e dati
    df.rename(columns={"Strumento finanziario": "Strumento_finanziario",
              "Giorni restanti all'UGT": "Giorni_rimanenti"}, inplace=True)
    print(df)
    df['Delta'] = df['Delta'].astype(float)
    df['Deltasigned'] = df['Delta'].astype(float)
    df['Giorni_rimanenti'] = df['Giorni_rimanenti'].astype(int)

    df["Deltaabs"] = abs(df['Delta'].astype(float))
    df["Posizione"] = df['Posizione'].astype(int)
    df['Simbolo_solo'] = df['Strumento_finanziario'].str.split(' ').str[0]
    # eseguo la selezione
    df1 = df.loc[(df['Deltaabs'] < 0.075) & (df['Posizione'] < 0)]
    df["Deltariga"] = df["Delta"]*df['Posizione']*100

    # li ordino
    df4 = df.sort_values(by=['Deltaabs'],  ascending=False)
    # raggruppa il dataframe per il campo "campo1" e somma i valori per ogni gruppo
    df_grouped = df4.groupby('Simbolo_solo')['Deltariga'].sum().reset_index()

    # seleziona solo le righe con valori maggiori di 50 in 'Deltariga'
    df_grouped.sort_values(by=['Deltariga'], inplace=True, ascending=False)

    df_grouped.loc['Totale Delta'] = df_grouped.sum(numeric_only=True, axis=0)

    trades = df_grouped
    return render(request, "index4.html", {'trades': trades})

def analisi_bilanciamento_delta_titolo_scadenza(request):
    # vorrei riscrivere la routine esattamente come quella sopra solo che invece che raggruppare per simbolo_solo
    # raggruppo per simbolo_scadenza , cioeà i primi due campi di strumento finanziario e poi sommo i valori di deltariga
    # e poi li ordino per deltariga discendente
    # inporto df
    fruits = ['Totale Delta Portafoglio  ']
    template = loader.get_template('index4.html')
    # inporto df
    df = pd.read_csv('portfolio.csv')

    # aggiustamenti colonne e dati
    df.rename(columns={"Strumento finanziario": "Strumento_finanziario",
              "Giorni restanti all'UGT": "Giorni_rimanenti"}, inplace=True)
    print(df)
    df['Delta'] = df['Delta'].astype(float)
    df['Deltasigned'] = df['Delta'].astype(float)
    df['Giorni_rimanenti'] = df['Giorni_rimanenti'].astype(int)

    df["Deltaabs"] = abs(df['Delta'].astype(float))
    df["Posizione"] = df['Posizione'].astype(int)
    df['Simbolo_solo'] = df['Strumento_finanziario'].str.split(' ').str[0]
    # eseguo la selezione
    df1 = df.loc[(df['Deltaabs'] < 0.075) & (df['Posizione'] < 0)]
    df["Deltariga"] = df["Delta"]*df['Posizione']*100

    df['Simbolo_scadenza'] = df['Strumento_finanziario'].str.split(' ').str[0] + df['Strumento_finanziario'].str.split(' ').str[1]

    # li ordino
    df4 = df.sort_values(by=['Deltaabs'],  ascending=False)
    # raggruppa il dataframe per il campo "campo1" e somma i valori per ogni gruppo
    df_grouped = df4.groupby('Simbolo_scadenza')['Deltariga'].sum().reset_index()

    # seleziona solo le righe con valori maggiori di 35 in 'Deltariga'
    df_grouped.sort_values(by=['Deltariga'], inplace=True, ascending=False)



    
    #df_grouped.sort_values(by=['Simbolo_scadenza'], inplace=True, ascending=True)
   
    df_grouped.loc['Totale Delta'] = df_grouped.sum(numeric_only=True, axis=0)

    trades = df_grouped
    return render(request, "index4.html", {'trades': trades})






def analisi_opzioni_potenzialmente_da_rollare(request):
    template = loader.get_template('index5.html')
    # inporto df
    df = pd.read_csv('portfolio.csv')
    df2 = pd.DataFrame()

    # aggiustamenti colonne e dati
    df.rename(columns={"Strumento finanziario": "Strumento_finanziario",
              "Giorni restanti all'UGT": "Giorni_rimanenti"}, inplace=True)
    df['Delta'] = df['Delta'].astype(float)
    df['Giorni_rimanenti'] = df['Giorni_rimanenti'].astype(int)

    df["Deltaabs"] = abs(df['Delta'].astype(float))

    df["Valore temporale (%)"].replace("", 99.999, inplace=True)

    df["Valore_tmp_fin"] = df["Valore temporale (%)"].str.extract(
        r"(\d+\.\d+)")
    df["Valore_tmp_fin_float"] = df["Valore_tmp_fin"].astype(float)
    df['PUT/CALL'] = df['Strumento_finanziario'].str.split(' ').str[3]
    df["Posizione_int"] = df['Posizione'].astype(float)

    # df2 = df.loc[(df['Deltaabs'] > 0.35)  &  (df['Deltaabs'] < 0.50)     & (df["Posizione_int"] ) < 0 ]
    df2 = df.loc[(df['Deltaabs'] > 0.35) & (df['Deltaabs'] < 0.50)]
    print(df2)

    # seleziona righe con valore di 'Posizione_int' minore di 0 e 'Giorni_rimanenti' minore di 55

    df3 = df2.loc[(df["Posizione_int"]) < 0]
    df4 = df3.loc[(df['Giorni_rimanenti']) < 55]

    # li ordino per delta discendente
    df4.sort_values(by=['Deltaabs'], inplace=True, ascending=False)

    trades = df4
    return render(request, "index4.html", {'trades': trades})


def opzioni_da_vedere_se_andare_invertito(request):
    template = loader.get_template('index5.html')
    # inporto df
    df = pd.read_csv('portfolio.csv')
    df2 = pd.DataFrame()

    # aggiustamenti colonne e dati
    df.rename(columns={"Strumento finanziario": "Strumento_finanziario",
              "Giorni restanti all'UGT": "Giorni_rimanenti"}, inplace=True)
    df['Delta'] = df['Delta'].astype(float)
    df['Giorni_rimanenti'] = df['Giorni_rimanenti'].astype(int)

    df["Deltaabs"] = abs(df['Delta'].astype(float))

    df["Valore temporale (%)"].replace("", 99.999, inplace=True)

    df["Valore_tmp_fin"] = df["Valore temporale (%)"].str.extract(
        r"(\d+\.\d+)")
    df["Valore_tmp_fin_float"] = df["Valore_tmp_fin"].astype(float)
    df['PUT/CALL'] = df['Strumento_finanziario'].str.split(' ').str[3]

    df2 = df.loc[(df['Giorni_rimanenti'] < 12) & (
        df['Deltaabs'] > 0.5) ]
            
    trades = df2
    return render(request, "index4.html", {'trades': trades})





# QUESTO NON FUNZIONA PUOI RISCRIVERMI LA funziona analis di portafolgio vedendo dove è l'errore?

def analisi_di_portafoglio(request):
    template = loader.get_template('index7.html')
    # inporto df
    df = pd.read_csv('portfolio.csv')
    print(df)

    # aggiustamenti colonne e dati
    df.rename(columns={"Strumento finanziario": "Strumento_finanziario",
              "Giorni restanti all'UGT": "Giorni_rimanenti"}, inplace=True)

    df['Delta'] = df['Delta'].astype(float)
    df['Giorni_rimanenti'] = df['Giorni_rimanenti'].astype(int)

    df["Deltaabs"] = abs(df['Delta'].astype(float))

    df["Valore temporale (%)"].replace("", 99.999, inplace=True)

    df["Val_tmp_fin"] = df["Valore temporale (%)"].str.extract(r"(\d+\.\d+)")
    df["Val_tmp_fin_float"] = df["Val_tmp_fin"].astype(float)
    df['PUT/CALL'] = df['Strumento_finanziario'].str.split(' ').str[3]
    df['Simbolo_solo'] = df['Strumento_finanziario'].str.split(' ').str[0]

    df['Simbolo_solo_allineato'] = df['Simbolo_solo'].str.normalize(
        'NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    df['Simbolo_solo_allineato'] = df['Simbolo_solo'].str.lstrip()
    df['Strumento_finanziario'] = df['Strumento_finanziario'].str.lstrip()

    for index, row in df.iterrows():
        campo = row['Simbolo_solo_allineato']
        if campo.startswith(' '):
            campo = campo[1:]
        df.at[index, 'Simbolo_solo_allineato'] = campo

    print(df)

    df2 = df.loc[(df['Giorni_rimanenti'] < 30) & (df['Deltaabs'] > 0.5)]
    df3 = df.loc[(df['Val_tmp_fin_float'] < 1.5) & (df['Deltaabs'] > 0.5)]

    df4 = pd.concat([df2, df3])

    print(df)
    print(df4)

    for i in df4.index:
        stringa = str(df4.loc[i, 'Simbolo_solo_allineato'])
        print("ciclo"+stringa)
        reperisci_corrente_prezzo(stringa)
        stringa0 = str(stringa.iloc[0]) if isinstance(
            stringa, pd.Series) else str(stringa)

        stock = yf.Ticker(stringa0)
        price = stock.info['currentPrice']
        df4.at[i, 'current_price'] = price

    print(df4)
    fruits = ['riepilogo delle opzioni ']

    # analisi del portafoglio
    for i in df4.index:
        var = row['Simbolo_solo_allineato']
        # se il simbolo è diverso da IWM e anche da SPY
        if var != 'IWM' and var != 'SPY':
        
            try:
                stringa = str(df4.loc[i, 'Simbolo_solo'])
                print("ciclo"+stringa)
                stock = yf.Ticker(stringa)
                price = stock.info['currentPrice']
                pricefloat = float(price)
                simbolo = df['Strumento_finanziario'][i].split(' ')[0]
                data = df['Strumento_finanziario'][i].split(' ')[1]
                strike = df['Strumento_finanziario'][i].split(' ')[2]
                strikefloat = float(strike)
                putcall = df['Strumento_finanziario'][i].split(' ')[3]
                valore_temporale = df["Val_tmp_fin_float"][i]
                valore_temporale_float = float(valore_temporale)
                var = "ATTENZIONE La opzione è ITM " + simbolo + \
                    "    " + data + "    " + strike + "    " + putcall

                # print("prezzo" + pricefloat + "strike" +  strikefloat)
                if ((pricefloat < strikefloat) & (putcall == 'PUT')):
                    fruits.append(var)
                    if (valore_temporale_float < 1.0):
                        fruits.append(
                            "ATTENZIONE !!!! alto rischio di assegnazione")

                if ((pricefloat > strikefloat) & (putcall == 'CALL')):
                    fruits.append(var)
                    if (valore_temporale_float < 1.0):
                        fruits.append(
                            "ATTENZIONE !!!! alto rischio di assegnazione")

            except Exception:
                print(traceback.format_exc())
                # or
                print(sys.exc_info()[2])

    # eliminazione colonne
    df4 = df4.drop(['Operazione ticker'], axis=1)
    df4 = df4.drop(['Val_tmp_fin_float'], axis=1)
    df4 = df4.drop(['Unnamed: 15'], axis=1)

    #
    # ordina per giorni rimaneti e delta discendente
    df4.sort_values(by=['Giorni_rimanenti', 'Delta'],
                    inplace=True, ascending=False)

    return render(request, "index7.html", {'fruits': fruits})


def calcolo_theta_portafoglio(request):
    template = loader.get_template('index7.html')
    # inporto df
    df = pd.read_csv('portfolio.csv')

    Total = df['Theta portafoglio'].sum()

    fruits = ['Totale Theta Portafoglio  ', Total]

    return render(request, "index7.html", {'fruits': fruits})


def calcolo_totale_valore_temporale(request):
    template = loader.get_template('index7.html')
    # inporto df
    df = pd.read_csv('portfolio.csv')

    df["Posizione_int"] = df['Posizione'].astype(int)
    df["Valore temporale (%)"].replace("", 99.999, inplace=True)
    df["Val_tmp_fin"] = df["Valore temporale (%)"].str.extract(r"(\d+\.\d+)")
    df["Val_tmp_fin_float"] = df["Val_tmp_fin"].astype(float)
    df["Val_tmp_fin_float_Totale_riga"] = df["Val_tmp_fin_float"] * \
        100*df["Posizione_int"]

    Total = df['Val_tmp_fin_float_Totale_riga'].sum()

    fruits = ['Totale Valore temporale di Portafoglio  ', Total]

    return render(request, "index7.html", {'fruits': fruits})


def reperisci_corrente_prezzo(stringa0):
    stock = yf.Ticker(stringa0)
    price = stock.info['currentPrice']
    print("il prezzo è di", price)


def calcolo_di_quanto_itm(strike_price, prezzo_corrente, putcall):
    # vorrei esprimere in un a percentuale di quanto è itm un determinato prezzo di una azione rispetto allo strike price
    # che io posseggo e naturalmente dal fatto se sia PUT o CALL

    # se putcall è uguale a CALL
    if (putcall == 'CALL'):
        # calcolo la differenza tra prezzo corrente e strike price
        differenza = prezzo_corrente - strike_price
        # calcolo la percentuale di quanto è itm
        percentuale_itm = differenza/strike_price
        # calcolo la percentuale di quanto è itm
        percentuale_itm = percentuale_itm*100
        # arrotondo a due decimali
        percentuale_itm = round(percentuale_itm, 2)
        # restituisco la percentuale
        return percentuale_itm

    # se putcall è uguale a PUT
    else:
        # calcolo la differenza tra prezzo corrente e strike price
        differenza = strike_price - prezzo_corrente
        # calcolo la percentuale di quanto è itm
        percentuale_itm = differenza/strike_price
        # calcolo la percentuale di quanto è itm
        percentuale_itm = percentuale_itm*100
        # arrotondo a due decimali
        percentuale_itm = round(percentuale_itm, 2)
        # restituisco la percentuale
        return percentuale_itm

    # se putcall è diverso da CALL e da PUT
    return 0


def nuova_analisi_di_portafoglio(request):

    template = loader.get_template('index7.html')
    # inizializza schiera errori
    fruits = []
    itm = []
    bep = []
    operazioni = []

    # inporto df
    df = pd.read_csv('portfolio.csv')

    # aggiustamenti colonne e dati
    df.rename(columns={"Strumento finanziario": "Strumento_finanziario",
              "Giorni restanti all'UGT": "Giorni_rimanenti"}, inplace=True)

    df['Simbolo_solo'] = df['Strumento_finanziario'].str.split(' ').str[0]

    df['Simbolo_solo_allineato'] = df['Simbolo_solo'].str.normalize(
        'NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    df['Simbolo_solo_allineato'] = df['Simbolo_solo'].str.lstrip()
    # mi serve per dopo il prezzo di strike in formato float
    # il prezzo di strike è il terzo elemento della stringa Strumento finanziario in formato float
    # mi server il terzo elemento di Strumento finanziario
    # reperisco dal campo Strumento finanziario il prezzo di strike , cioè il terzo elemento
    # della stringa e lo converto in float e lo aggiungo al data frame
    df['strikefloat2'] = df['Strumento_finanziario'].str.split(
        ' ').str[2].astype(float)
    #

    # lettura del dataframe e reperimento del prezzo
    for index, row in df.iterrows():
        var = row['Simbolo_solo_allineato']
        # se il simbolo è diverso da IWM e anche da SPY
        if var != 'IWM' and var != 'SPY':
            # eseguo la routine
            stock = yf.Ticker(var)
            price = stock.info['currentPrice']
            # print(stock)
            # print(price)
            # reperisco dal campo Strumento finanziario il prezzo di strike , cioè il terzo elemento
            # della stringa e lo converto in float
            strike = row['Strumento_finanziario'].split(' ')[2]
            strikefloat = float(strike)
            # aggiungo la colonna strikefloat al data frame
            df.at[index, 'strikefloat'] = strikefloat
            # aggiungo la colonna price al data frame e lo converto in float
            df.at[index, 'price'] = price
            pricefloat = float(price)
            # aggiungo la colonna pricefloat al data frame
            df.at[index, 'pricefloat'] = pricefloat
            # aggiungo la colonna PUTCALL al data frame e reperisco dal campo Strumento finanziario il tipo di opzione , cioè il quarto elemento
            # della stringa
            putcall = row['Strumento_finanziario'].split(' ')[3]
            df.at[index, 'putcall'] = putcall
            # ho bisogno di unire i primi due campi di Strumento finanziario
            simbolo = row['Strumento_finanziario'].split(' ')[0]
            simbolo = simbolo + row['Strumento_finanziario'].split(' ')[1]
            df.at[index, 'simbolo'] = simbolo
            #

    # azzero la variabile comunque
    prezzo_medio_opzione_comprata = 0
    differenza = 0
    break_even_point = 0

    print(df)

    # lettura del dataframe e reperimento del prezzo
    for index, row in df.iterrows():
        var = row['Simbolo_solo_allineato']
        if var != 'IWM':

            # se posizione è minore di zero, reperisco tutte le opzioni vendute
            if (row['Posizione'] < 0):

                simbolo = row['simbolo']
                putcall = row['putcall']
                # lancio una routine alla quale passo simbolo e putcall e restituisce il prezzo medio
                prezzo_medio_opzione_comprata = reperisci_premio_opzione_comprata2(
                    simbolo, putcall, df)
                strike_opzione_comprata = reperisci_strike_opzione_comprata(
                    simbolo, putcall, df)

                # a questo punto prendo il prezzo corrente e gli sottraggo prezzo medio opzione comprata e basta
                differenza = row['Pr. medio'] - prezzo_medio_opzione_comprata
                # aggiungo la colonna differenza al data frame
                df.at[index, 'differenza'] = differenza
                # a questo punto calcolo il break even point della riga e lo aggiungo al data frame
                if (putcall == 'CALL'):
                    # calcolo il break even point della riga e lo aggiungo al data frame
                    # devo prendere il prezzo dello strike in float e sommare la differenza
                    break_even_point = row['strikefloat'] + differenza
                else:
                    # calcolo il break even point della riga e lo aggiungo al data frame
                    # devo prendere il prezzo dello strike in float e sottrarre la differenza
                    break_even_point = row['strikefloat'] - differenza
                # aggiungo la colonna break_even_point al data frame

                df.at[index, 'break_even_point'] = break_even_point

                # eseguo l'elaborazione
                # reperisco il prezzo corrente
                prezzo_corrente = row['pricefloat']
                prezzo_correntestringa = str(prezzo_corrente)

                # reperisco il prezzo di strike
                strike = row['strikefloat']

                # reperisco il valore di quanto è in the money chiamando la routine reperisci_quanto_in_the_money
                quanto_in_the_money = calcolo_di_quanto_itm(
                    strike, prezzo_corrente, putcall)
                totale_premio_incassato_per_simbolo = reperisci_premio_totale_simbolo(
                    simbolo, df)

                # totale valore a rischio per simbolo
                totale_valore_a_rischio_per_simbolo = totale_premio_incassato_per_simbolo - \
                    abs((strike - strike_opzione_comprata)
                        * abs(row['Posizione'])*100)
                print(simbolo, putcall, strike, strike_opzione_comprata,
                      totale_premio_incassato_per_simbolo, totale_valore_a_rischio_per_simbolo)

                # se putcall è uguale a CALL
                if (putcall == 'CALL'):
                    # se prezzo corrente è maggiore di strike ma minore di break_even_point
                    if (prezzo_corrente >= strike) & (prezzo_corrente <= break_even_point):
                     # aggiungi a fruits il seguernte messaggio " il titolo "  + simbolo + " è tra il prezzo di strike e il B/E point"
                     # fruits.append('il titolo ' + row['Strumento_finanziario'] + ' è tra il prezzo di strike e il B/E point: ' + '    prezzo corrente   ' + prezzo_correntestringa  +  '   B/E point   ' + str(break_even_point))
                        bep.append('il titolo ' + row['Strumento_finanziario'] + ' è tra il prezzo di strike e il B/E point: ' + '    prezzo corrente   ' +
                                   prezzo_correntestringa + '   B/E point   ' + str(break_even_point) + '  giorni rimanenti  ' + str(row['Giorni_rimanenti']) + '  quanto in the money  ' + str(quanto_in_the_money) + '%' + '  tot.premio x simbolo  ' + str(totale_premio_incassato_per_simbolo) + '  tot.valore a rischio x simbolo  ' + str(totale_valore_a_rischio_per_simbolo))
                        # se i giorni rimanenti sono minori di 21
                        if (row['Giorni_rimanenti'] < 21):
                            operazioni.append(
                                'bisogna intervenire su ' + row['Strumento_finanziario'] + ' perchè i giorni rimanenti sono minori di 21')

                    if (prezzo_corrente > break_even_point):
                        # aggiungi a fruits il seguernte messaggio " il titolo "  + simbolo + " ha superato il B/E point"
                        # fruits.append('il titolo ' + row['Strumento_finanziario'] + ' ha superato il B/E point: ' + '    prezzo corrente   ' + prezzo_correntestringa  +  '   B/E point   ' + str(break_even_point))
                        itm.append('il titolo ' + row['Strumento_finanziario'] + ' ha superato il B/E point: ' + '    prezzo corrente   ' +
                                   prezzo_correntestringa + '   B/E point   ' + str(break_even_point) + '  giorni rimanenti  ' + str(row['Giorni_rimanenti']) + '  quanto in the money  ' + str(quanto_in_the_money) + '%' + '  tot.premio x simbolo  ' + str(totale_premio_incassato_per_simbolo) + '  tot.valore a rischio x simbolo  ' + str(totale_valore_a_rischio_per_simbolo))
                        # se i giorni rimanenti sono minori di 21
                        if (row['Giorni_rimanenti'] < 21):
                            operazioni.append(
                                'bisogna intervenire su ' + row['Strumento_finanziario'] + ' perchè i giorni rimanenti sono minori di 21')

                # se putcall è uguale a PUT
                else:
                    # se prezzo corrente è minore di strike ma maggiore di break_even_point
                    if (prezzo_corrente <= strike) & (prezzo_corrente >= break_even_point):
                        # aggiungi a fruits il seguernte messaggio " il titolo "  + simbolo + " è tra il prezzo di strike e il B/E point"
                        # fruits.append('il titolo ' + row['Strumento_finanziario'] + ' è tra il prezzo di strike e il B/E point: ' + '    prezzo corrente   ' + prezzo_correntestringa  +  '   B/E point   ' + str(break_even_point))
                        bep.append('il titolo ' + row['Strumento_finanziario'] + ' è tra il prezzo di strike e il B/E point: ' + '    prezzo corrente   ' +
                                   prezzo_correntestringa + '   B/E point   ' + str(break_even_point) + '  giorni rimanenti  ' + str(row['Giorni_rimanenti']) + '  quanto in the money  ' + str(quanto_in_the_money) + '%' + '  tot.premio x simbolo  ' + str(totale_premio_incassato_per_simbolo) + '  tot.valore a rischio x simbolo  ' + str(totale_valore_a_rischio_per_simbolo))
                        # se i giorni rimanenti sono minori di 21
                        if (row['Giorni_rimanenti'] < 21):
                            operazioni.append(
                                'bisogna intervenire su ' + row['Strumento_finanziario'] + ' perchè i giorni rimanenti sono minori di 21')
                    if (prezzo_corrente < break_even_point):
                        # aggiungi a fruits il seguernte messaggio " il titolo "  + simbolo + " ha superato il B/E point"
                        # fruits.append('il titolo ' + row['Strumento_finanziario'] + ' ha superato il B/E point: ' + '    prezzo corrente   ' + prezzo_correntestringa  +  '   B/E point   ' + str(break_even_point))
                        itm.append('il titolo ' + row['Strumento_finanziario'] + ' ha superato il B/E point: ' + '    prezzo corrente   ' +
                                   prezzo_correntestringa + '   B/E point   ' + str(break_even_point) + '  giorni rimanenti  ' + str(row['Giorni_rimanenti']) + '  quanto in the money  ' + str(quanto_in_the_money) + '%' + '  tot.premio x simbolo  ' + str(totale_premio_incassato_per_simbolo) + '  tot.valore a rischio x simbolo  ' + str(totale_valore_a_rischio_per_simbolo))
                        # se i giorni rimanenti sono minori di 21
                        if (row['Giorni_rimanenti'] < 21):
                            operazioni.append(
                                'bisogna intervenire su ' + row['Strumento_finanziario'] + ' perchè i giorni rimanenti sono minori di 21')

            else:
                df.at[index, 'break_even_point'] = 0

    print(df)

    # aggiungo un elemento vuoto a bep
    bep.append('')
    #
    # aggiungo gli elementi di bep e itm a fruits
    fruits = fruits + bep + itm

    return render(request, "index7.html", {'fruits': fruits})


def reperisci_premio_opzione_comprata2(simbolop, putcallp, df):

    # azzero variabile prezzo medio
    prezzo_medio_long = 0
    # loop sul dataframe
    for index, row in df.iterrows():

        # se simbolo passsato alla routine è uguale a simbolo nel df e putcallp è uguale a putcall e la posizione è > di 0
        # allora ho trovato l'opzione comprata
        if (simbolop == row['simbolo']) & (putcallp == row['putcall']) & (row['Posizione'] > 0):
            # reperisco il prezzo medio
            prezzo_medio_long = row['Pr. medio']

    return prezzo_medio_long


def reperisci_strike_opzione_comprata(simbolop, putcallp, df):

    # azzero variabile prezzo medio
    strike = 0
    # loop sul dataframe
    for index, row in df.iterrows():

        # se simbolo passsato alla routine è uguale a simbolo nel df e putcallp è uguale a putcall e la posizione è > di 0
        # allora ho trovato l'opzione comprata
        if (simbolop == row['simbolo']) & (putcallp == row['putcall']) & (row['Posizione'] > 0):
            # reperisco il prezzo medio
            strike = row['strikefloat']

    return strike


def ultimate_analisi_di_portafoglio(request):
    # inizializza il template
    template = loader.get_template('index7.html')
    # inizializza schiera errori
    fruits = []
    # inizializza il dataframe
    df = pd.read_csv('Analisi_trade.csv')

    df['Simbolo_solo'] = df['Simbolo'].str.split(' ').str[0]
    df.sort_values(by=['Simbolo_solo'], inplace=True)

    # raggruppa il dataframe per il campo "Simbolo_opzione" e somma i valori per ogni gruppo
    df_grouped = df.groupby('Simbolo_solo')

    print(df_grouped)

    return render(request, "index7.html", {'fruits': fruits})


def reperisci_premio_totale_simbolo(simbolop, df):

    # azzero variabile prezzo medio
    valore = 0

    # loop sul dataframe
    for index, row in df.iterrows():

        # se simbolo passsato alla routine è uguale a simbolo nel df
        # allora ho trovato l'opzione comprata
        if (simbolop == row['simbolo']):
            # reperisco il prezzo medio
            valore = valore + row['Pr. medio'] * row['Posizione']*100

    # arrotondo a due decimali e lo porto comunque ad un valore positivo
    valore = abs(round(valore, 2))
    # restituisco il valore

    return valore




#-------------------------------------------------------------------------------------------
def analisi_opzioni_vendute_comprate(request):
    df = pd.read_csv('Analisi_trade.csv')

    df2 = df.drop(
        ["Sommario profitti e perdite Realizzati e Non realizzati", "Header"], axis=1)
    df2 = df.drop(["Realizzato Profitto S/T",
                  "Realizzato Perdita S/T"], axis=1)
    
    df['PUT/CALL'] = df['Simbolo'].str.split(' ').str[3]
    
    # ordina per put call
    df2.sort_values(by=['PUT/CALL'], inplace=True, ascending=False)

    trades = df2
   
    return render(request, "index4.html", {'trades': trades})



def analisi_operazioni(request):
    df = pd.read_csv('Analisi_operazioni.csv')

    # escludo dal dataframe le righe che sono di tipo Subtotal
    df = df[df['Header'] != 'Subtotal']
    # escludo dal dataframe le righe che sono di tipo Total
    df = df[df['Header'] == 'Data']

    # aggiungo al data frame le colonne PUT/CALL e Simbolo_solo, strike e data scadenza e le popolo
    df['PUT/CALL'] = df['Simbolo'].str.split(' ').str[3]
    df['Simbolo_solo'] = df['Simbolo'].str.split(' ').str[0]
    df['Strike'] = df['Simbolo'].str.split(' ').str[2]
    df['Data_scadenza'] = df['Simbolo'].str.split(' ').str[1]

    # elimino quelli che hanno simbolo solo = a EUR.USD 
    df = df[df['Simbolo_solo'] != 'EUR.USD']
   
    # converto il campo Quantità in intero
    df['Quantità'] = df['Quantità'].str.replace(',', '').astype(int)
    
    # df1 sono le operazioni di tipo PUT comprate( quando la quantita è Maggiore di 0
    # e il tipo di opzione è PUT)
    df1 = df[(df['Quantità'] > 0) & (df['PUT/CALL'] == 'P')]
    # df2 sono le operazioni di tipo PUT vendute( quando la quantita è Minore di 0
    # e il tipo di opzione è PUT)
    df2 = df[(df['Quantità'] < 0) & (df['PUT/CALL'] == 'P')]
    # df3 sono le operazioni di tipo CALL comprate( quando la quantita è Maggiore di 0
    # e il tipo di opzione è CALL)
    df3 = df[(df['Quantità'] > 0) & (df['PUT/CALL'] == 'C')]
    # df4 sono le operazioni di tipo CALL vendute( quando la quantita è Minore di 0
    # e il tipo di opzione è CALL)
    df4 = df[(df['Quantità'] < 0) & (df['PUT/CALL'] == 'C')]

    print(df1)
    print(df2)
    print(df3)
    print(df4)

 
   
   
    trades = df1
   
    return render(request, "index4.html", {'trades': trades})


def analisi_operazioni_di_un_determinato_mese(request):
    template = loader.get_template('index9.html')


    return render(request, "index9.html")


def analisi_operazioni_di_un_determinato_mese_esecuzione(request):
    template = loader.get_template('index9.html')

    df = pd.read_csv('Analisi_trade.csv')

    # estraggo il primo campo di simbolo
    
    print(df)
    
    # estraggo quelli che in simbolo_solo_mese hanno il valore che c'è nella combobox data_scadenza
    # estraggo il valore selzionato nella combobox
    data_scadenza = request.POST.get('data_scadenza')
    print("questa è la data scadenza")
    print(data_scadenza)
    # estraggo quelli che in simbolo_solo_mese hanno il valore che c'è nella combobox data_scadenza
    df = df[df['Simbolo_solo_mese'] == data_scadenza]
    # a simbolo_solo_mese elimino tutti i caratteri a destra e a sinistra che non sono blank
    df['Simbolo_solo_mese'] = df['Simbolo_solo_mese'].str.strip()
      
    
   

    print(df)

    # ragguppo per simbolo solo facendo il totale di P/L realizzato
    df_grouped = df.groupby('Simbolo_solo')['P/L realizzato'].sum()
    # aggiungo una riga con il totale finale
    df_grouped.loc['Total'] = df_grouped.sum()

          
    print(df_grouped)

    trades = df
   
    return render_to_response('index.html', context_instance=RequestContext(request))
    return render(request, "index4.html", {'trades': trades})


   



def analisi_opzioni_con_il_minore_Theta(request):
    df = pd.read_csv('portfolio.csv')

    # aggiustamenti colonne e dati
    df.rename(columns={"Strumento finanziario": "Strumento_finanziario",
                "Giorni restanti all'UGT": "Giorni_rimanenti"}, inplace=True)
    
    # vado a vedere le opzioni che hanno il minore theta

    # prendo il THeta e lo converto in float
    df["Theta_float"] = df['Theta'].astype(float)
    # prendo il valore assoluto di Theta
    df["Thetaabs"] = df['Theta_float'].abs()
    # calcolo il theta a giorno e lo aggiungo al data frame e lo arrotondo a due decimali
    df["Theta_gg"] = df["Thetaabs"] *100
    df["Theta_gg"] = round(df["Theta_gg"], 2)

    

    # prendo solo quelli che hanno il theta assoluto minere di 0.08 e scadenza  minore di 21 giorni e posizione minore di 0
    df = df[df['Thetaabs'] < 0.08]
    
    # df = df[df['Giorni_rimanenti'] < 45]
    df = df[df['Posizione'] < 0]
    

    # ordino per theta
    df.sort_values(by=['Theta'], inplace=True, ascending=False)
    
    # le visulaizzo su html

    trades = df

    return render(request, "index4.html", {'trades': trades})


def analisi_dei_movimenti_anno(request):
    template = loader.get_template('index4.html')
    # inporto df
    df = pd.read_csv('Movimenti_anno.csv')
    print(df)


    # estarggo il primo campo di simbolo
    df['Simbolo_solo'] = df['Simbolo'].str.split(' ').str[0]

    # esttraggo il quarto campo di simbolo PUT/CALL
    df['PUT/CALL'] = df['Simbolo'].str.split(' ').str[3]

    # il campo p/l realizzato lo converto in float a due decimali
    df["P/L realizzato"] = df['P/L realizzato'].astype(float)
    df["P/L realizzato"] = round(df["P/L realizzato"], 2)
    

    # estraggo il campo simbolo+data
    df['Simbolo_solo_mese'] = df['Simbolo'].str.split(' ').str[0] + \
        df['Simbolo'].str.split(' ').str[1]
    
    # prendo solo quelli che hanno il simbolo solo_mese uguale a 'AAPL 17FEB23'
    df = df[df['Simbolo_solo_mese'] == 'TXN15SEP23']
    
    # li ordino per data ora di esecuzione in modo ascendente
    df.sort_values(by=['Data/ora'], inplace=True, ascending=True)

    # alla fine del dataframe aggiungo una riga con il totale di solo il campo P/L realizzato
    totale = df['P/L realizzato'].sum()
    
    # aggiungo una riga con il totale con il metodo concat al df
    df = pd.concat([df, pd.DataFrame(
        [[totale]], columns=df.columns)], ignore_index=True)
   

    
    trades = df

    return render(request, "index4.html", {'trades': trades})
