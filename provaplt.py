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

# estraggo il secondo campo di simbolo 
df['Scadenza'] = df['Simbolo'].str.split(' ').str[1]

# faccio un ripilogo dei dati per scadenza  e con solo il realizzato totale e lo memorizzo in un df
df2 = df.groupby(['Scadenza'])['Realizzato Totale'].sum().to_frame()
 

df2.plot()
plt.show()
