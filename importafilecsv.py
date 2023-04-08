#-------------------------------------------------------------------------------------
# lettura file csv. proveniente da Interactive Brokers
#
#
#-------------------------------------------------------------------------------------
import pandas as pd
df = pd.read_csv('trade.csv')
print(df)


df = df.assign(d_minus_a = df['Proceeds Sold'] - df['Proceeds Bought'])

for column in df:
   print(column)

print(df)

