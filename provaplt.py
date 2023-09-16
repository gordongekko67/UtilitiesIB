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
 

df.plot()
plt.show()
