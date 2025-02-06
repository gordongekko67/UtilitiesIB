
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
    df = pd.read_csv('portfoliook.csv')

    # aggiustamenti colonne e dati
    df.rename(columns={"Strumento finanziario": "Strumento_finanziario",
              "Giorni restanti all'UGT": "GG_rim"}, inplace=True)
    print(df)
    df['Delta'] = df['Delta'].astype(float)
    df['GG_rim'] = df['GG_rim'].astype(int)

    df["Deltaabs"] = abs(df['Delta'].astype(float))

    # la colonna dei giorni va vicino alla colonna del valore temporale
    df = df[['Strumento_finanziario',  'GG_rim',         'Valore temporale (%)', 'Ultimo', 'Posizione',
                'Delta', 'Deltaabs', 'Variazione %', 'Modifica']]

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
    df = pd.read_csv('portfoliook.csv')

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

    # la colonna dei giorni va vicino alla colonna del valore temporale
    df1 = df1[['Strumento_finanziario', 'Valore temporale (%)',  'GG_rim', 'Valore_tmp_fin', 'Valore_tmp_fin_float',
                'Ultimo',  'Posizione', 'Delta', 'Deltaabs', 'Variazione %', 'Modifica']]

    # li ordino
    df4 = df1.sort_values(['Valore_tmp_fin_float'],
                          ascending=[True])

    # emissione videata
    trades = df4
    return render(request, "index4.html", {'trades': trades})












def importa_portfolio_ITM_valore_temporale_2(request):
    template = loader.get_template('index4.html')
    # inporto df
    df = pd.read_csv('portfoliook.csv')

    # aggiustamenti colonne e dati
    df.rename(columns={"Strumento finanziario": "Strumento_finanziario",
              "Giorni restanti all'UGT": "GG_rim"}, inplace=True)
    print(df)
    df['Delta'] = df['Delta'].astype(float)
    df['GG_rim'] = df['GG_rim'].astype(int)

    df["Deltaabs"] = abs(df['Delta'].astype(float))
    df["Posizione"] = df['Posizione'].astype(int)

    # eseguo la selezione con deltaabs > 0.499999 e GG_rim < 25 e Posizione < 0
    df1 = df.loc[(df['Deltaabs'] > 0.499999) & (df['GG_rim'] < 25) & (df['Posizione'] < 0)]
             
    # estraggo il primo campo del valore temporale e lo converto in float
    df1["Valore temporale (%)"].replace("", 99.999, inplace=True)

    df1["Valore_tmp_fin"] = df1["Valore temporale (%)"].str.extract(
        r"(\d+\.\d+)")
    df1["Valore_tmp_fin_float"] = df1["Valore_tmp_fin"].astype(float)

    # elimino la colonna simbolo_solo e operazione ticker
    df1.drop(["Operazione ticker"], axis=1, inplace=True)

    # la colonna dei giorni va vicino alla colonna del valore temporale
    df1 = df1[['Strumento_finanziario', 'Valore temporale (%)',  'GG_rim', 'Valore_tmp_fin', 'Valore_tmp_fin_float',
                'Ultimo',  'Posizione', 'Delta', 'Deltaabs', 'Variazione %', 'Modifica']]

    # li ordino
    df4 = df1.sort_values(['Valore_tmp_fin_float'],
                          ascending=[True])

    # emissione videata
    trades = df4
    return render(request, "index4.html", {'trades': trades})




def importa_portfolio_ITM_valore_temporale_percentuale(request):
    template = loader.get_template('index4.html')
    # inporto df
    df = pd.read_csv('portfoliook.csv')

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
 
def elevatissimo_rischio_di_assegnazione(request):
    template = loader.get_template('index5.html')
    # inporto df
    df = pd.read_csv('portfoliook.csv')
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

    # ricavo la posizione
    df["Posizione"] = df['Posizione'].astype(int)

    # prendo solo le righe con valore temporale < 0.5

    df2 = df.loc[(df['Deltaabs'] > 0.499) & (df['Valore_tmp_fin_float'] < 0.99) & (df['Posizione'] < 0)]

    
    # li ordino per valore temporale crescente
    df4 = df2.sort_values(['Valore_tmp_fin_float'],
                            ascending=[True])
    

    # emissione videata
    trades = df4
    print(trades)
    return render(request, "index5.html", {'trades': trades})


    



def importa_portfolio_con_rischio_di_assegnazione(request):
    template = loader.get_template('index5.html')
    # inporto df
    df = pd.read_csv('portfoliook.csv')
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
    df = pd.read_csv('portfoliook.csv')

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

def analisi_prendere_profitto(request):
    template = loader.get_template('index4.html')
    # inporto df
    df = pd.read_csv('portfoliook.csv')

    # aggiustamenti colonne e dati
    df.rename(columns={"Strumento finanziario": "Strumento_finanziario",
              "Giorni restanti all'UGT": "Giorni_rimanenti"}, inplace=True)
    print(df)
    df['Delta'] = df['Delta'].astype(float)
    df['Giorni_rimanenti'] = df['Giorni_rimanenti'].astype(int)

    df["Deltaabs"] = abs(df['Delta'].astype(float))
    df["Posizione"] = df['Posizione'].astype(int)
    df["P&L non realizzato"] = df['P&L non realizzato'].astype(str)
    df["P&L non realizzato_float"] = df['P&L non realizzato'].str.extract(
        r"(\d+\.\d+)")
    df["P&L non realizzato_float"] = df["P&L non realizzato_float"].astype(float)
          
    # metto il campo P&L non realizzato in prima posizione
    df = df[['P&L non realizzato', 'Strumento_finanziario', 'Giorni_rimanenti', 'Ultimo', 'Posizione',
                'Delta', 'Deltaabs', 'Variazione %', 'Modifica']]
        
    # elimino eventuali caratteri , da P&L non realizzato
    df['P&L non realizzato'] = df['P&L non realizzato'].str.replace(',', '')
    df['P&L non realizzato'] = df['P&L non realizzato'].astype(float)
    
    # eseguo la selezione
    # prendo quelli con deltaabs > 0.5 e P/L non realizzato > 0
    df1 = df.loc[(df['Deltaabs'] > 0.499999) & (df['Posizione'] < 0) & (df['P&L non realizzato'] > 100)]

    # li ordino
    df4 = df1.sort_values(by=['P&L non realizzato'],  ascending=False)

    # emissione videata
    trades = df4

    return render(request, "index4.html", {'trades': trades})



def analisi_prendere_profitto_2(request):
    
    template = loader.get_template('index4.html')
    # inporto df
    df = pd.read_csv('portfoliook.csv')

    # aggiustamenti colonne e dati
    df.rename(columns={"Strumento finanziario": "Strumento_finanziario",
              "Giorni restanti all'UGT": "Giorni_rimanenti"}, inplace=True)
    print(df)
    df['Delta'] = df['Delta'].astype(float)
    df['Giorni_rimanenti'] = df['Giorni_rimanenti'].astype(int)

    df["Deltaabs"] = abs(df['Delta'].astype(float))
    df["Posizione"] = df['Posizione'].astype(int)
    df["P&L non realizzato"] = df['P&L non realizzato'].astype(str)
    df["P&L non realizzato_float"] = df['P&L non realizzato'].str.extract(
        r"(\d+\.\d+)")
    df["P&L non realizzato_float"] = df["P&L non realizzato_float"].astype(float)
          
    # metto il campo P&L non realizzato in prima posizione
    df = df[['P&L non realizzato', 'Strumento_finanziario', 'Giorni_rimanenti', 'Ultimo', 'Posizione',
                'Delta', 'Deltaabs', 'Variazione %', 'Modifica']]
        
    # elimino eventuali caratteri , da P&L non realizzato
    df['P&L non realizzato'] = df['P&L non realizzato'].str.replace(',', '')
    df['P&L non realizzato'] = df['P&L non realizzato'].astype(float)
    
    # eseguo la selezione
    # prendo quelli con deltaabs > 0.5 e P/L non realizzato > 0
    df1 = df.loc[(df['Deltaabs'] < 0.16499999) & (df['Posizione'] < 0) & (df['P&L non realizzato'] > 100)]

    # li ordino
    df4 = df1.sort_values(by=['P&L non realizzato'],  ascending=False)

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

    '''
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
   '''
       

    # emissione videata
    return render(request, "index4.html", {'trades': trades})


def analisi_trade_scadenza_2(request):
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

    # estraggo il campo scadenza
    df2['Scadenza'] = df['Simbolo'].str.split(' ').str[1]   

    df2[(df2.Scadenza == '15DEC23') | (df2.Scadenza == '19JAN24') | (df2.Scadenza == '16FEB24') | (df2.Scadenza == '15MAR24')]


    # elimino delle righe che non mi servono 
    df2 = df2[~((df2.Simbolo_solo == 'IWM') & (df2.Scadenza == '15MAR24'))]
    df2 = df2[~((df2.Simbolo_solo == 'JNJ') & (df2.Scadenza == '21JUN24'))]
    df2 = df2[~((df2.Simbolo_solo == 'MRK') & (df2.Scadenza == '19JAN24'))]
   


    print(df2)


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

    '''
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
   '''
       

    # emissione videata
    return render(request, "index4.html", {'trades': trades})














def analisi_trade_scadenza_PUTCALL(request):
    df = pd.read_csv('Analisi_trade.csv')
    df2 = df.drop(
        ["Sommario profitti e perdite Realizzati e Non realizzati", "Header"], axis=1)

    df2['Simbolo_solo'] = df['Simbolo'].str.split(' ').str[0]
    df2['Simbolo_opzione'] = df['Simbolo'].str.split(
        ' ').str[0] + df['Simbolo'].str.split(' ').str[1]
    
    # prendo il quarto elemento di Simbolo che sarebbe se CALL o PUT
    df2['Tipo_CALL_PUT'] = df['Simbolo'].str.split(' ').str[3]

    # creo un nuovo campo con simbolo opzione e tipo call put
    df2['Simbolo_opzione_tipo'] = df2['Simbolo_opzione'] + df2['Tipo_CALL_PUT']

    df2.sort_values(by=['Simbolo_opzione_tipo'], inplace=True)

    # lo raggruppo per simbolo opzione e tipo call put e totalizzo tutto 
    df_grouped = df2.groupby(['Simbolo_opzione_tipo']).agg(
        {'Realizzato Totale': 'sum', 'Non realizzato Totale': 'sum', 'Totale': 'sum'}).reset_index()
    

    trades = df_grouped[['Simbolo_opzione_tipo',
                            'Realizzato Totale', 'Non realizzato Totale', 'Totale']]
    
    # ordine per totale
    trades = trades.sort_values(by=['Totale'],  ascending=True)
    
    # visualizzo in html
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
                                                                     'SEP', 'OCT', 'NOV', 'DEC'], ['01 Gennaio', '02 Febbraio', '03 Marzo', '04 Aprile', '05 Maggio', '06 Giugno', '07 Luglio', '08 Agosto',
                                                                                                    '09 Settembre', '10 Ottobre', '11 Novembre', '12 Dicembre'])
                                                                                     
        
                                                                                                   

    
    # estraggo da data scadenza solo l'anno che sarebbe solo il sesto e settimo carattere
    df2['Data_scadenza_anno'] = df2['Data_scadenza'].str[6:7]

    # estraggo data scadenza anno estesa = se Data_scadenza_anno = 3 allora 2023, ecc ecc
    df2['Data_scadenza_anno_estesa'] = df2['Data_scadenza_anno'].replace(['3', '4', '5', '6', '7', '8', '9', '0'], ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'])

    # estraggo il mese come Jan feb ecc ecc
    df2['Data_scadenza_mese_estesa'] = df2['Data_scadenza_mese'].replace(['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG',
                                                                        'SEP', 'OCT', 'NOV', 'DEC'], ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu', 'Lug', 'Ago',
                                                                                                        'Set', 'Ott', 'Nov', 'Dic'])
    
    # aggiungo un campo con datascadenza_anno_estesa + datascadenza_mese_estesa
    df2['Data_scadenza_mese_anno_numero'] = df2['Data_scadenza_anno_estesa'] + " " + df2['Data_scadenza_mese_numero']

    
    # li ordino per data_scadenza_mese_anno_estesa crescente 
    df2.sort_values(by=['Data_scadenza_mese_anno_numero', 'Simbolo_solo'], inplace=True)

    # raggruppa il dataframe per il campo "Data_scadenza_mese_anno" e "Simbolo_solo" e somma i valori per ogni gruppo
    # a cambiamento di data_scadenza_mese_anno devo fare un totale
    df_grouped = df2.groupby(['Data_scadenza_mese_anno_numero']).agg(
        {'Realizzato Totale': 'sum', 'Non realizzato Totale': 'sum', 'Totale': 'sum'}).reset_index()
    
    trades = df_grouped[['Data_scadenza_mese_anno_numero', 'Realizzato Totale', 'Non realizzato Totale', 'Totale']]

    # faccio un totale finale
    trades.loc['Totale'] = trades.sum(numeric_only=True, axis=0)
    
    #df2.plot()
    #plt.show()
  


    #       
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




def analisi_trade_scadenza_simbolo_ancora_aperte_ordinate_per_mese(request):
    # devo fare lo stesso di analisi_trade_scadenza_simbolo_ancora_aperte
    #solo che invece che riepilogare e ordinare per simbolo_opzione devo riepilogare e ordinare per mese-simbolo_opzione
    
    df = pd.read_csv('Analisi_trade.csv')
    df2 = df.drop(
        ["Sommario profitti e perdite Realizzati e Non realizzati", "Header"], axis=1)
    
    print(df2)
    
    # estraggo da data scadenza che e' il secondo campo di simbolo 
    df2['Data_scadenza'] = df['Simbolo'].str.split(' ').str[1]
    # estraggo il titolo che e' il primo campo di simbolo
    df2['Simbolo_solo'] = df['Simbolo'].str.split(' ').str[0]
    
    # creo un nuovo campo con data_scadenza + simbolo_solo
    df2['Data_scadenza_solo'] = df2['Data_scadenza'] + " " + df2['Simbolo_solo']

    # adesso ordino e raggruppo tutto per data_scadenza_solo
    df2.sort_values(by=['Data_scadenza_solo'], inplace=True)
    # raggruppa il dataframe per il campo "Data_scadenza_solo" e somma i valori per ogni gruppo
    df_grouped = df2.groupby('Data_scadenza_solo').agg(
        {'Realizzato Totale': 'sum', 'Non realizzato Totale': 'sum', 'Totale': 'sum'}).reset_index()
    trades0 = df_grouped[['Data_scadenza_solo',
                            'Realizzato Totale', 'Non realizzato Totale', 'Totale']]
    trades = trades0.sort_values(by=['Data_scadenza_solo'],  ascending=True)

    # devo prendere di trades solo le righe con non realizzato diverso da 0
    trades = trades[trades['Non realizzato Totale'] != 0]

    # faccio una somma finale per avere il totale del realizzato e non realizzato Totale
    trades.loc['Totale'] = trades.sum(numeric_only=True, axis=0)


    # emissione videata
    return render(request, "index4.html", {'trades': trades})

def analisi_trade_scadenza_simbolo_specifica(request):
    # devo fare lo stesso di analisi_trade_scadenza_simbolo_ancora_aperte
    #solo che invece che riepilogare e ordinare per simbolo_opzione devo riepilogare e ordinare per mese-simbolo_opzione
    
    df = pd.read_csv('Analisi_trade.csv')
    df2 = df.drop(
        ["Sommario profitti e perdite Realizzati e Non realizzati", "Header"], axis=1)
    
    print(df2)
  
    
    # estraggo da data scadenza che e' il secondo campo di simbolo 
    df2['Data_scadenza'] = df['Simbolo'].str.split(' ').str[1]
    # estraggo il titolo che e' il primo campo di simbolo
    df2['Simbolo_solo'] = df['Simbolo'].str.split(' ').str[0]
    
    # creo un nuovo campo con data_scadenza + simbolo_solo
    df2['Data_scadenza_solo'] = df2['Data_scadenza'] + " " + df2['Simbolo_solo']

    # adesso ordino e raggruppo tutto per data_scadenza_solo
    df2.sort_values(by=['Data_scadenza_solo'], inplace=True)
    # raggruppa il dataframe per il campo "Data_scadenza_solo" e somma i valori per ogni gruppo
    
    trades = df2[df2['Data_scadenza_solo'] == '15DEC23 IWM']
    # metti i totali a fine dataframe
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
    df = pd.read_csv('portfoliook.csv')

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
    df = pd.read_csv('portfoliook.csv')

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
    df = pd.read_csv('portfoliook.csv')
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
    df = pd.read_csv('portfoliook.csv')
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
    df['PUT/CALL'] = df['Strumento_finanziario'].str.split(' ').str[3]

    # anche la quantità deve essere negativa
    df["Posizione_int"] = df['Posizione'].astype(float)

    # se giorni < di 50 e delta > 0.5

    df2 = df.loc[(df['GG'] <  50)  & (df['Deltaabs'] > 0.5) & (df["Posizione_int"] < 0)]  
    
    # faccio un loop su questi elelmnti e vado a reperire il prezzo corrente
    for index, row in df2.iterrows():

        # se il simbolo è diverso da IWM e anche da SPY e anche da USD e anche da QQQ
        # e anche da TLT e anche da GLD e anche da SLV e anche da VXX e anche da VIXY
        # e anche da VIXM e anche da VIX e anche da VIXW e anche da VIX3M e anche da VIX6M

        if df2['Strumento_finanziario'][index].split(' ')[0] != 'IWM' and df2['Strumento_finanziario'][index].split(' ')[0] != 'SPY' and df2['Strumento_finanziario'][index].split(' ')[0] != 'USD' and df2['Strumento_finanziario'][index].split(' ')[0] != 'QQQ' and df2['Strumento_finanziario'][index].split(' ')[0] != 'TLT' and df2['Strumento_finanziario'][index].split(' ')[0] != 'GLD' and df2['Strumento_finanziario'][index].split(' ')[0] != 'SLV' and df2['Strumento_finanziario'][index].split(' ')[0] != 'VXX' and df2['Strumento_finanziario'][index].split(' ')[0] != 'VIXY' and df2['Strumento_finanziario'][index].split(' ')[0] != 'VIXM' and df2['Strumento_finanziario'][index].split(' ')[0] != 'VIX' and df2['Strumento_finanziario'][index].split(' ')[0] != 'VIXW' and df2['Strumento_finanziario'][index].split(' ')[0] != 'VIX3M' and df2['Strumento_finanziario'][index].split(' ')[0] != 'VIX6M':                              
            # con simbolo solo vado a predenermi il ticker su yahoo finance
            simbolo_solo = df2['Strumento_finanziario'][index].split(' ')[0]
            # vado a prednere il prezzo su yahho  finance
            ticker = yf.Ticker(simbolo_solo)
            print(simbolo_solo)
            # prendo il prezzo
            prezzo = ticker.info['currentPrice']
            # lo inserisco nel dataframe nella terza colonna
            df2.at[index, 'Prezzo_corrente'] = prezzo
            
    
    # la colonna prezzo corrente me la porto all'inizio
    df2 = df2[['Strumento_finanziario', 'Prezzo_corrente', 'GG','Deltaabs', 'Valore temporale (%)', 'Valore_tmp_fin', 'Valore_tmp_fin_float', 'PUT/CALL', 'Posizione', 'Posizione_int']]
                                           
                 
    # li ordino per valore finanziario crescente
    df2.sort_values(by=['Valore_tmp_fin_float'], inplace=True, ascending=True)

     
   
            
    trades = df2
    return render(request, "index4.html", {'trades': trades})





# QUESTO NON FUNZIONA PUOI RISCRIVERMI LA funziona analis di portafolgio vedendo dove è l'errore?

def analisi_di_portafoglio(request):
    template = loader.get_template('index7.html')
    # inporto df
    df = pd.read_csv('portfoliook.csv')
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
        # prendo il primo campo di strumento finanziario
        stringa = df['Strumento_finanziario'][i].split(' ')[0]
        # se il simbolo è diverso da IWM e anche da SPY e anche da QQQ
        if stringa != 'IWM' and stringa != 'SPY' and stringa != 'QQQ':

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
        if var != 'IWM' and var != 'SPY' and var != 'QQQ':     
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
    #df4 = df4.drop(['Unnamed: 15'], axis=1)

    #
    # ordina per giorni rimaneti e delta discendente
    df4.sort_values(by=['Giorni_rimanenti', 'Delta'],
                    inplace=True, ascending=False)

    return render(request, "index7.html", {'fruits': fruits})


def calcolo_theta_portafoglio(request):
    template = loader.get_template('index7.html')
    # inporto df
    df = pd.read_csv('portfoliook.csv')

    Total = df['Theta portafoglio'].sum()

    fruits = ['Totale Theta Portafoglio  ', Total]

    return render(request, "index7.html", {'fruits': fruits})


def analisi_delle_LEAP_options(request):
    template = loader.get_template('index7.html')
    # inporto df
    df = pd.read_csv('portfoliook.csv')

    # aggiustamenti colonne e dati
    df.rename(columns={"Strumento finanziario": "Strumento_finanziario",
                "Giorni restanti all'UGT": "Giorni_rimanenti"}, inplace=True)
    
    #  giorni rimanaenti deve essere convertito in in int
    df['Giorni_rimanenti'] = df['Giorni_rimanenti'].astype(int)

    # prendo quelli che hanno giorni rimanenti > 100
    df2 = df.loc[(df['Giorni_rimanenti'] > 100)]

    # li ordino per delta 
    
    df2.sort_values(by=['Delta'], inplace=True, ascending=False)
    
    
    # emissione videata
    trades = df2
    return render(request, "index4.html", {'trades': trades})






def calcolo_totale_valore_temporale(request):
    template = loader.get_template('index7.html')
    # inporto df
    df = pd.read_csv('portfoliook.csv')

    df["Posizione_int"] = df['Posizione'].astype(int)
    df["Valore temporale (%)"].replace("", 99.999, inplace=True)
    df["Val_tmp_fin"] = df["Valore temporale (%)"].str.extract(r"(\d+\.\d+)")
    df["Val_tmp_fin_float"] = df["Val_tmp_fin"].astype(float)
    df["Val_tmp_fin_float_Totale_riga"] = df["Val_tmp_fin_float"] * \
        100*df["Posizione_int"]

    Total = df['Val_tmp_fin_float_Totale_riga'].sum()

    fruits = ['Totale Valore temporale di Portafoglio  ', Total]

    return render(request, "index7.html", {'fruits': fruits})





def calcolo_totale_valore_temporale_residuo_per_scadenza(request):
    template = loader.get_template('index4.html')
    # inporto df
    df = pd.read_csv('portfoliook.csv')

    df["Posizione_int"] = df['Posizione'].astype(int)
    df["Valore temporale (%)"].replace("", 99.999, inplace=True)
    df["Val_tmp_fin"] = df["Valore temporale (%)"].str.extract(r"(\d+\.\d+)")
    df["Val_tmp_fin_float"] = df["Val_tmp_fin"].astype(float)
    df["Val_tmp_fin_float_Totale_riga"] = df["Val_tmp_fin_float"] * \
        100*df["Posizione_int"]
    
    df["Deltaabs"] = abs(df['Delta'].astype(float))
    
    # creo due nuovi campi che mi servono per il raggruppamento
    # se deltaabs è minore di 0.5 allora metto in Valore_tmp_fin_float_totale riga_OTM il valore di Valore_tmp_fin_float_totale riga
    # altrimenti metto 0
    df.loc[df['Deltaabs'] < 0.5, 'Valore_tmp_fin_float_Totale_riga_OTM'] = df['Val_tmp_fin_float_Totale_riga']

    # se deltaabs è maggiore di 0.5 allora metto in Valore_tmp_fin_float_totale riga_ITM il valore di Valore_tmp_fin_float_totale riga
    # altrimenti metto 0
    df.loc[df['Deltaabs'] > 0.5, 'Valore_tmp_fin_float_Totale_riga_ITM'] = df['Val_tmp_fin_float_Totale_riga']

            
    # aggiustamenti colonne e dati
    df.rename(columns={"Strumento finanziario": "Strumento_finanziario",
              "Giorni restanti all'UGT": "Giorni_rimanenti"}, inplace=True)
    

    # visualizzo nel data frame solo le colonne che mi servono : strumento finanziario, giorni rimanenti, deltaabs, valore temporale, valore temporale float, valore temporale float totale riga
    df = df[['Strumento_finanziario', 'Giorni_rimanenti', 'Deltaabs', 'Valore temporale (%)', 'Val_tmp_fin', 'Val_tmp_fin_float_Totale_riga', 'Valore_tmp_fin_float_Totale_riga_ITM', 'Valore_tmp_fin_float_Totale_riga_OTM']]        



    
    # ordino per scadenza e strumento finanziario
    df.sort_values(by=['Giorni_rimanenti', 'Strumento_finanziario'], inplace=True, ascending=True)

    # a cambio data scadenza faccio un totale per totale riga ITM e OTM
    df_grouped = df.groupby('Giorni_rimanenti').agg(
        {'Valore_tmp_fin_float_Totale_riga_ITM': 'sum', 'Valore_tmp_fin_float_Totale_riga_OTM': 'sum'}).reset_index()
    
    
    # e un totale finale solo di valori temporali
    df_grouped.loc['Totale'] = df_grouped.sum(numeric_only=True, axis=0)

    # aggiungo i totali di valori temporali (append non è supportato)
    df_grouped.loc['Totale', 'Valore_tmp_fin_float_Totale_riga_ITM'] = df_grouped['Valore_tmp_fin_float_Totale_riga_ITM'].sum()

    trades = df 
    

    
    return render(request, "index4.html", {'trades': trades})

def reperisci_corrente_prezzo(stringa0):
    stock = yf.Ticker(stringa0)
    print('il valore di stringa0 è'+stringa0)
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
    df = pd.read_csv('portfoliook.csv')

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
    template = loader.get_template('index4.html')
    # inizializza schiera errori
    fruits = []
    # inizializza il dataframe
    df = pd.read_csv('portfoliook.csv')

    # devo estrarre il primo campo di simbolo
    df['Simbolo_solo'] = df['Strumento finanziario'].str.split(' ').str[0]
    

    # creo un nuovo dataframe con solo simbolo_solo raggruppato 
    # 
    df2 = df.groupby(['Simbolo_solo']).agg({'Posizione': 'sum'}).reset_index()

    # per ognuno dei simboli di df2 vado a reperire il prezzo tramite yahoo finance tranne che per IWM, SPY e QQQ
    for index, row in df2.iterrows():
        var = row['Simbolo_solo']
        # se il simbolo è diverso da IWM e anche da SPY
        if var != 'IWM' and var != 'SPY' and var != 'QQQ':
            # eseguo la routine
            stock = yf.Ticker(var)
            price = stock.info['currentPrice']
            # aggiungo la colonna price al data frame e lo converto in float
            df2.at[index, 'price'] = price
            pricefloat = float(price)
            # aggiungo la colonna pricefloat al data frame
            df2.at[index, 'pricefloat'] = pricefloat

    
    print(df2)

    # prendo i primi due ampi di Strumento finanziario e li unisco
    df['Simbolo_solo_data'] = df['Strumento finanziario'].str.split(' ').str[0] + df['Strumento finanziario'].str.split(' ').str[1]
    # creo un nuovo dataframe con solo simbolo_solo_data  raggruppato e totalizzo per delta di portafoglio , riportando nella riga anche simbolo_solo
    df3 = df.groupby(['Simbolo_solo_data']).agg({'Delta portafoglio': 'sum', 'Simbolo_solo': 'first'}).reset_index()
    # aggiungo al data frame df3 la colonna Simbolo_solo

    # aggiungo al data frame df3 la colonna pricefloat aggiungendo la colonna pricefloat di df2
    df3['pricefloat'] = df3['Simbolo_solo'].map(df2.set_index('Simbolo_solo')['pricefloat'])
    # aggiungo al data frame df3 la colonna price aggiungendo la colonna price di df2
    df3['price'] = df3['Simbolo_solo'].map(df2.set_index('Simbolo_solo')['price'])

    # faccio il merge di df  con  df3 agganciandomi a simbolo_solo_data e prendendo i campi di df3 delta portafoglio, pricefloat e price
    df4 = pd.merge(df, df3[['Simbolo_solo_data', 'Delta portafoglio', 'pricefloat', 'price']], on='Simbolo_solo_data', how='left')

    
    print(df4)

    df4['Valore_temporale_float'] = df4['Valore temporale (%)'].str.split(' ').str[0].astype(float)

    # metto delta portafoglio e price nella terza e quarta colonna
    df4.insert(3, 'Delta portafoglio_y', df4.pop('Delta portafoglio_y'))
    df4.insert(4, 'pricefloat', df4.pop('pricefloat'))
    df4.insert(5, 'valore_temporale_float', df4.pop('Valore_temporale_float'))

    
    

    # creo un nuovo dataframe che prende :
    # 1) le righe che hanno delta in valore assuluto maggiore di 0.50 e la posizione è minore di 0 e il valore temporale è minore di 1.2
      # anche il valore 00.000 è minore di 1.2
    # 2) le righe che hanno delta in valore assuluto minore di 0.50 e la posizione è maggiore di 0 e il valore temporale è minore di 1.2

    print(df4)

    # prendo delta in valore assoluto e in float
    df4['Deltaabs'] = abs(df4['Delta'].astype(float))

    # prendo posizione in float
    df4['Posizione'] = df4['Posizione'].astype(float)

    print(df4)


    df5 = df4[(df4['Deltaabs'] > 0.50) & (df4['Posizione'] < 0) ]

    # ordino per Valore temporale_float crescente
    df5.sort_values(by=['Valore_temporale_float'], inplace=True, ascending=True)
    
      

      

    

    
    


    print(df5)

    trades = df5
   
    return render(request, "index4.html", {'trades': trades})



def ultimate_analisi_di_portafoglio_2(request):
    # inizializza il template
    template = loader.get_template('index4.html')
    # inizializza il dataframe
    df1 = pd.read_csv('portfoliook.csv')

    trades = df1
    print(trades)
   
    return render(request, "index4.html", {'trades': trades})



  



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

def visualizza_tutte_le_opzioni_long(request):
    df = pd.read_csv('portfoliook.csv')

    # aggiustamenti colonne e dati
    df.rename(columns={"Strumento finanziario": "Strumento_finanziario",
                "Giorni restanti all'UGT": "Giorni_rimanenti"}, inplace=True)

    # visulaizza solo le opzioni long ordinate per GG di scadenza
    df = df[df['Posizione'] > 0]

    # ordino per Strumento
    df.sort_values(by=['Strumento_finanziario'], inplace=True, ascending=True)
       
    trades = df

    return render(request, "index4.html", {'trades': trades})

def analisi_opzioni_con_il_maggiore_gamma(request):

    df = pd.read_csv('portfoliook.csv')

    # aggiustamenti colonne e dati
    df.rename(columns={"Strumento finanziario": "Strumento_finanziario",
                "Giorni restanti all'UGT": "Giorni_rimanenti"}, inplace=True)

    # vado a vedere le opzioni che hanno il maggiore gamma

    # prendo il gamma e lo converto in float
    df["Gamma_float"] = df['Gamma'].astype(float)
    # calcolo il gamma a giorno e lo aggiungo al data frame e lo arrotondo a due decimali
    df["Gamma_gg"] = df["Gamma_float"] *100
    df["Gamma_gg"] = round(df["Gamma_gg"], 2)

    

    # prendo solo quelli che hanno il gamma maggiore di 0.08 e scadenza  minore di 21 giorni e posizione maggiore di 0
    df = df[df['Gamma_float'] > 0.04]
    
    # df = df[df['Giorni_rimanenti'] < 45]
    df = df[df['Posizione'] < 0]
    

    # ordino per gamma
    df.sort_values(by=['Gamma_float'], inplace=True, ascending=False)
    
    # le visulaizzo su html

    trades = df

    return render(request, "index4.html", {'trades': trades})


def analisi_opzioni_con_il_maggiore_vega(request):

    df = pd.read_csv('portfoliook.csv')

    # aggiustamenti colonne e dati
    df.rename(columns={"Strumento finanziario": "Strumento_finanziario",
                "Giorni restanti all'UGT": "Giorni_rimanenti"}, inplace=True)

    # vado a vedere le opzioni che hanno il maggiore gamma

    # prendo il gamma e lo converto in float
    df["Vega_float"] = df['Vega'].astype(float)
   
       
    
    # prendo solo quelli che hanno il vega  maggiore di 0.10 
    df = df[df['Vega_float'] > 0.10]
    

    # ordino per gamma
    df.sort_values(by=['Vega_float'], inplace=True, ascending=False)
    
    # le visulaizzo su html

    trades = df

    return render(request, "index4.html", {'trades': trades})





def analisi_opzioni_con_il_minore_Theta(request):
    df = pd.read_csv('portfoliook.csv')

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

      
    # elimino le righe che nella colonna 'Header' non sono di tipo data
    df = df[df['Header'] == 'Data']

    # elimino le prime 4 colonne che non mi servono
    df = df.drop(['Dettaglio eseguiti', 'Tipo di attivo',
                    'Header', 'DataDiscriminator'], axis=1)

          
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
    
    print(df)
    
    # prendo solo quelli che hanno il simbolo solo_mese uguale a 'AAPL 17FEB23'
    df = df[df['Simbolo_solo_mese'] == 'MSFT21MAR25']
    
    # li ordino per data ora di esecuzione in modo ascendente
    df.sort_values(by=['Data/ora'], inplace=True, ascending=True)

    avviso = 'Attenzione i totali non sono completi in quanto mancano le opzioni comprate andate in scadenza'

    # alla fine del data frame aggiungo una dicitura " attenzione i totali non sono completi in quanto mancano le opzioni comprate andate in scadenza"
    # la aggiungo con il comando concat
    df = pd.concat([df, pd.DataFrame([[avviso]], columns=['Data/ora'])], ignore_index=True)

    trades = df

    return render(request, "index4.html", {'trades': trades})

def analisi_dei_movimenti_anno_2(request):
    template = loader.get_template('index4.html')
    # inporto df
    df = pd.read_csv('Movimenti_anno.csv')


    # Seleziona solo le righe dove il valore della prima colonna non è "Statement"
    df = df[df.iloc[:, 0] != "Statement"]

    # Salva il DataFrame risultante in un nuovo file CSV
    df.to_csv('Movimenti_anno.csv', index=False)

          
    # elimino le righe che nella colonna 'Header' non sono di tipo data
    df = df[df['Header'] == 'Data']

    # elimino le prime 4 colonne che non mi servono
    df = df.drop(['Dettaglio eseguiti', 'Tipo di attivo',
                    'Header', 'DataDiscriminator'], axis=1)


    # estarggo il secondo campo di simbolo
    df['Data scadenza'] = df['Simbolo'].str.split(' ').str[1]

    # prendo solo quelli che hanno  data scadenza = 201023
    df = df[df['Data scadenza'] == '21JUN24']

    # li ordino per data ora di esecuzione in modo ascendente
    df.sort_values(by=['Data/ora'], inplace=True, ascending=True)

    avviso = 'Attenzione i totali non sono completi in quanto mancano le opzioni comprate andate in scadenza'
    # faccio un totale finale di P/L realizzato
    totale_pl_realizzato = df['P/L realizzato'].sum()
    # arrotondo a due decimali
    totale_pl_realizzato = round(totale_pl_realizzato, 2)  



    # alla fine del data frame aggiungo avvio e totale al dataframe
    # la aggiungo con il comando concat
    df = pd.concat([df, pd.DataFrame([[avviso, totale_pl_realizzato]], columns=['Data/ora', 'P/L realizzato'])], ignore_index=True)

    trades = df
    

    return render(request, "index4.html", {'trades': trades})




def analisi_dei_movimenti_anno_3(request):
    template = loader.get_template('index4.html')
    # inporto df
    df = pd.read_csv('Movimenti_anno.csv')
    print(df)

      
    # elimino le righe che nella colonna 'Header' non sono di tipo data
    df = df[df['Header'] == 'Data']

    # elimino le prime 4 colonne che non mi servono
    df = df.drop(['Dettaglio eseguiti', 'Tipo di attivo',
                    'Header', 'DataDiscriminator'], axis=1)


    # estarggo il primo campo di  simbolo
    df['Simbolo_solo'] = df['Simbolo'].str.split(' ').str[0]
    # prendo solo quelli che hanno  simbolo = a 
    df = df[df['Simbolo_solo'] == 'IWM']

    # li ordino per data ora di esecuzione in modo ascendente
    df.sort_values(by=['Data/ora'], inplace=True, ascending=True)

    avviso = 'Attenzione i totali non sono completi in quanto mancano le opzioni comprate andate in scadenza'
    # faccio un totale finale di P/L realizzato
    totale_pl_realizzato = df['P/L realizzato'].sum()
    # arrotondo a due decimali
    totale_pl_realizzato = round(totale_pl_realizzato, 2)  



    # alla fine del data frame aggiungo avvio e totale al dataframe
    # la aggiungo con il comando concat
    df = pd.concat([df, pd.DataFrame([[avviso, totale_pl_realizzato]], columns=['Data/ora', 'P/L realizzato'])], ignore_index=True)

    trades = df
    

    return render(request, "index4.html", {'trades': trades})


def analisi_dei_movimenti_anno_4(request):
    template = loader.get_template('index4.html')
    # inporto df
    df = pd.read_csv('Movimenti_anno.csv')
    print(df)


    # Seleziona solo le righe dove il valore della prima colonna non è "Statement"
    df = df[df.iloc[:, 0] != "Statement"]

    # Salva il DataFrame risultante in un nuovo file CSV
    df.to_csv('Movimenti_anno.csv', index=False)


      
    # elimino le righe che nella colonna 'Header' non sono di tipo data
    df = df[df['Header'] == 'Data']

    # elimino le prime 4 colonne che non mi servono
    df = df.drop(['Dettaglio eseguiti', 'Tipo di attivo',
                    'Header', 'DataDiscriminator'], axis=1)


    # estarggo il primo campo di simbolo
    df['Simbolo_solo'] = df['Simbolo'].str.split(' ').str[0]

    # estarggo il secondo campo di simbolo
    df['Data scadenza'] = df['Simbolo'].str.split(' ').str[1]

    # prendo solo quelli che hanno  data scadenza = 201023
    df = df[df['Data scadenza'] == '19APR24']

     
    # li ordino per Simbolo_solo, Data scadenza, e Data/ora in modo ascendente
    df.sort_values(by=['Simbolo_solo', 'Data/ora'], inplace=True, ascending=True)


    avviso = 'Attenzione i totali non sono completi in quanto mancano le opzioni comprate andate in scadenza'
    # faccio un totale finale di P/L realizzato
    totale_pl_realizzato = 0
    # arrotondo a due decimali
    totale_pl_realizzato = round(totale_pl_realizzato, 2)  



    # alla fine del data frame aggiungo avvio e totale al dataframe
    # la aggiungo con il comando concat
    df = pd.concat([df, pd.DataFrame([[avviso, totale_pl_realizzato]], columns=['Data/ora', 'P/L realizzato'])], ignore_index=True)

    trades = df
    

    return render(request, "index4.html", {'trades': trades})





def analisi_delle_perdite(request):
    template = loader.get_template('index4.html')
    # inporto df
    df = pd.read_csv('Movimenti_anno.csv')
    print(df)

    # seleziono solo le righe che hanno il campo P/L realizzato minore di 0

    df = df[df['P/L realizzato'] < 0]

    # cancello le colonne : dettaglio eseguiti e tipo di attivo , header e data discriminator
    df = df.drop(['Dettaglio eseguiti', 'Tipo di attivo',
                  'Header', 'DataDiscriminator'], axis=1)


    # estraggo il quarto campo di simbolo PUT/CALL
    df['PUT/CALL'] = df['Simbolo'].str.split(' ').str[3]

    # estraggo il campo quantità e lo converto in intero
    df['Quantità'] = df['Quantità'].str.replace(',', '').astype(int)

    #  ordino per tipo put call/ e quantità

    df.sort_values(by=['PUT/CALL', 'Quantità'], inplace=True, ascending=True)
    # a faccio una riga di separazione tra put e call e tra quantità positiva e negativa
    
    # aggiungo un numeratore di riga che a rottura di put call si azzera
    df['numeratore'] = df.groupby(['PUT/CALL']).cumcount()+1

    
    

    trades = df

    return render(request, "index4.html", {'trades': trades})


# prova github 




def test_importazione(request):
    
    df = pd.read_csv('Analisi_trade.csv')

    

    df.plot()
    plt.show()






    




def analisi_di_una_determinata_posizione(request):
    template = loader.get_template('index10.html')

    # vado a stampare cosa c'è nel campo ticker di index10.html
    ticker = request.POST.get('ticker')
    print(ticker)

    return render(request, "index10.html")



def analisi_operazioni_vendute_comprate(request):
    df = pd.read_csv('Analisi_trade.csv')

    # estraggo il campo PUT/CALL dal quarto campo del simbolo 
    df['PUT/CALL'] = df['Simbolo'].str.split(' ').str[3]

    # df1  sono le operazioni di tipo PUT vendute (quando la posizione è minore  di 0
    # e il tipo di opzione è PUT)

    df1 = df[(df['Posizione'] < 0) & (df['PUT/CALL'] == 'P')]

    # df2  sono le operazioni di tipo CALL vendute (quando la posizione è minore  di 0
    # e il tipo di opzione è CALL)

    df2 = df[(df['Posizione'] < 0) & (df['PUT/CALL'] == 'C')]

    # df3  sono le operazioni di tipo PUT comprate (quando la posizione è maggiore  di 0
    # e il tipo di opzione è PUT)

    df3 = df[(df['Posizione'] > 0) & (df['PUT/CALL'] == 'P')]

    # df4  sono le operazioni di tipo CALL comprate (quando la posizione è maggiore  di 0
    # e il tipo di opzione è CALL)

    df4 = df[(df['Posizione'] > 0) & (df['PUT/CALL'] == 'C')]

    # faccio il describe dei 4 dataframe
    print(df1.describe())
    print(df2.describe())
    print(df3.describe())
    print(df4.describe())

    
def analisi_posizioni_da_rollare_prossima_scadenza(request):
    template = loader.get_template('index4b.html')
    # inporto df
    df = pd.read_csv('portfoliook.csv')
    # aggiustamenti colonne e dati
     # elimino eventuali caratteri , da P&L non realizzato
    df['Val mkt'] = df['Val mkt'].str.replace(',', '')
    # valore di mercato Val mrt lo porto ad essere un valore float
    df["Val mkt"] = df['Val mkt'].astype(float)
    # prendo tutti quelli che hanno i giorni rimanenti minori di 21
    df = df[df["Giorni restanti all'UGT"] < 21]

    # estraggo il primo campo di simbolo 
    df['Simbolo_solo'] = df['Strumento finanziario'].str.split(' ').str[0]
    # ordino per simbolo_solo
    df.sort_values(by=['Simbolo_solo'], inplace=True, ascending=True)
    # raggruppo per simbolo_solo e faccio la somma di val mkt
    df_grouped = df.groupby('Simbolo_solo')['Val mkt'].sum()
    # ordino df_grouped per val mkt crescente
    df_grouped.sort_values(inplace=True, ascending=True)
    # da df_groped prendo solo quelli che hanno val mkt minore di 0
    df_grouped = df_grouped[df_grouped < 0]
    # e li ordino in ordine decrescente
    df_grouped.sort_values(inplace=True, ascending=False)


    # aggiungo una riga con il totale finale
    df_grouped.loc['Total'] = df_grouped.sum()

    # stampo a video il dataframe
    print(df_grouped)

    trades = df_grouped
        

    return render(request, "index4b.html", {'trades': trades})
    


def analisi_di_portafoglio_parziale(request):
    
    template = loader.get_template('index4b.html')
    # inporto df
    df = pd.read_csv('portfoliook.csv')
    # aggiustamenti colonne e dati
     # elimino eventuali caratteri , da P&L non realizzato
    df['Val mkt'] = df['Val mkt'].str.replace(',', '')
    # valore di mercato Val mrt lo porto ad essere un valore float
    df["Val mkt"] = df['Val mkt'].astype(float)
   
    # estraggo il primo campo di simbolo 
    df['Simbolo_solo'] = df['Strumento finanziario'].str.split(' ').str[0]
    # ordino per simbolo_solo

    # prendo solo quelli che hanno simbolo solo = a TXN
    df = df[df['Simbolo_solo'] == 'TXN']

    # converto delta di portafoglio in un numero float
    df["Delta portafoglio"] = df['Delta portafoglio'].astype(float)
    
    # aggiungo una riga con il totlae di delta di portafoglio
    df.loc['Total'] = df.sum()
    
    # stampo a video il dataframe
    print(df)

    trades = df
        

    return render(request, "index4.html", {'trades': trades})

    
        




def analisi_di_portafoglio_2(request):


    template = loader.get_template('index4b.html')
    # inporto df
    df = pd.read_csv('portfoliook.csv')

    # aggiustamenti colonne e dati
     # elimino eventuali caratteri , da P&L non realizzato
    df['Val mkt'] = df['Val mkt'].str.replace(',', '')
    # valore di mercato Val mrt lo porto ad essere un valore float
    df["Val mkt"] = df['Val mkt'].astype(float)
   
    # estraggo il primo campo di simbolo 
    df['Simbolo_solo'] = df['Strumento finanziario'].str.split(' ').str[0]
    # ordino per simbolo_solo

    # converto delta di portafoglio in un numero float
    df["Delta portafoglio"] = df['Delta portafoglio'].astype(float)

    # estraggo il secondo campo scadenza
    df['Scadenza'] = df['Strumento finanziario'].str.split(' ').str[1]

    #unisco i due campi simbolo_solo + scadenza
    df['Simbolo_soloScadenza'] = df['Simbolo_solo'] + ' ' + df['Scadenza']


    # Raggruppa per Simbolo_soloScadenzae calcola la somma di Deltaportafoglio
    df2 = df.groupby('Simbolo_soloScadenza').agg({'Delta portafoglio': 'sum'}).reset_index()

    df2['delta_portafoglio_abs'] = df2['Delta portafoglio'].abs()
    df2["delta_portafoglio_abs"] = df2['delta_portafoglio_abs'].astype(float)
   
    # stampo a video il dataframe
    print(df2)

    # Filtraggio delle righe con delta_portafoglio_abs maggiore di 20
    filtered_df1 = df2[df2['delta_portafoglio_abs'] > 20]

    # Raggruppa per Simbolo
    df3 = df.groupby('Simbolo_solo').agg({'Delta portafoglio': 'sum'}).reset_index()

    df3['delta_portafoglio_abs'] = df3['Delta portafoglio'].abs()
    df3["delta_portafoglio_abs"] = df3['delta_portafoglio_abs'].astype(float)
   
    # stampo a video il dataframe
    print(df3)

    # Filtraggio delle righe con delta_portafoglio_abs maggiore di 20
    filtered_df3 = df3[df3['delta_portafoglio_abs'] > 20]

    # unisco i due data frame


    trades =  filtered_df3        

    return render(request, "index4.html", {'trades': trades})



def analisi_di_portafoglio_3(request):


    template = loader.get_template('index4b.html')
    # inporto df
    df = pd.read_csv('portfoliook.csv')

    # aggiustamenti colonne e dati
     # elimino eventuali caratteri , da P&L non realizzato
    df['Val mkt'] = df['Val mkt'].str.replace(',', '')
    # valore di mercato Val mrt lo porto ad essere un valore float
    df["Val mkt"] = df['Val mkt'].astype(float)
   
    # estraggo il primo campo di simbolo 
    df['Simbolo_solo'] = df['Strumento finanziario'].str.split(' ').str[0]
    # ordino per simbolo_solo

    # converto delta di portafoglio in un numero float
    df["Delta portafoglio"] = df['Delta portafoglio'].astype(float)

    # estraggo il secondo campo scadenza
    df['Scadenza'] = df['Strumento finanziario'].str.split(' ').str[1]

    #unisco i due campi simbolo_solo + scadenza
    df['Simbolo_soloScadenza'] = df['Simbolo_solo'] + ' ' + df['Scadenza']


    # Raggruppa per Simbolo_soloScadenzae calcola la somma di Deltaportafoglio
    df2 = df.groupby('Simbolo_soloScadenza').agg({'Delta portafoglio': 'sum'}).reset_index()

    df2['delta_portafoglio_abs'] = df2['Delta portafoglio'].abs()
    df2["delta_portafoglio_abs"] = df2['delta_portafoglio_abs'].astype(float)
   
    # stampo a video il dataframe
    print(df2)

    # Filtraggio delle righe con delta_portafoglio_abs maggiore di 20
    filtered_df1 = df2[df2['delta_portafoglio_abs'] > 20]

    # Raggruppa per Simbolo
    df3 = df.groupby('Simbolo_solo').agg({'Delta portafoglio': 'sum'}).reset_index()

    df3['delta_portafoglio_abs'] = df3['Delta portafoglio'].abs()
    df3["delta_portafoglio_abs"] = df3['delta_portafoglio_abs'].astype(float)
   
    # stampo a video il dataframe
    print(df3)

    # Filtraggio delle righe con delta_portafoglio_abs maggiore di 20
    filtered_df3 = df3[df3['delta_portafoglio_abs'] > 20]

    # unisco i due data frame


    trades =  filtered_df1        

    return render(request, "index4.html", {'trades': trades})



def analisi_di_anno_2024(request):


    template = loader.get_template('index4b.html')
    # inporto df
    df = pd.read_csv('movimenti_anno_2024op.csv')

    df_filtrato = df[~df['Header'].isin(['SubTotal', 'Total'])]


    # Calcola la somma della colonna 'P/L realizzato'
    somma_PL = df_filtrato['P/L realizzato'].sum()

    print(somma_PL)


    trades =  df_filtrato        

    return render(request, "index4.html", {'trades': trades})

