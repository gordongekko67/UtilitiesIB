import os
import sys
import pandas as pd
import matplotlib.pyplot as plt


# creaa un piccolo dataframe con i dati con una descrizione e pochi dati
df = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6, 7, 8, 9],
                     'b': [1, 2, 3, 4, 5, 6, 7, 8, 9],
                        'c': [1, 2, 3, 4, 5, 6, 7, 8, 9],

                        'd': [1, 2, 3, 4, 5, 6, 7, 8, 9],
                        'e': [1, 2, 3, 4, 5, 6, 7, 8, 9],
                        'f': [1, 2, 3, 4, 5, 6, 7, 8, 9],


                        'g': [1, 2, 3, 4, 5, 6, 7, 8, 9]})


# crea un grafico con i dati del dataframe
df.plot()
plt.show()

df = pd.read_csv('Analisi_trade.csv')
 
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

    # mi creo un nuovo dataframe da trades
    df5 = trades.copy()
    # stampo le caratteristiche di df5
    print(df5.info())
    print(df5.describe())

    # emetto un grafico con matplotlib a barre su di un diagramma cartesiano 
    # con asse x = Data_scadenza_mese_anno_numero e asse y = Totale
    # e faccio un grafico a punti con asse x = Data_scadenza_mese_anno_numero e asse y = Totale
    '''
    # copio il datframe in un altro per poterlo modificare con solo totale
    trades2 = trades.copy()
    # lascio solo la colonna totale
    trades2 = trades2[['Data_scadenza_mese_anno_numero', 'Totale']]

    # lo trasformo in numeri con due decimali per la visulaizzazione solo
    trades2['Totale'] = trades2['Totale'].round(2)
    # lo visualizzo con matplotlib
    trades2.plot.bar(x='Data_scadenza_mese_anno_numero', y=['Totale'], rot=0, figsize=(15, 10))
    # faccio un diagramma a punti
    trades2.plot(x='Data_scadenza_mese_anno_numero', y=['Totale'], kind='scatter', figsize=(15, 10)) 

    print(trades2)
    '''


    #       
