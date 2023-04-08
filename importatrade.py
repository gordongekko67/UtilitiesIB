#-------------------------------------------------------------------------------------
# lettura file csv. proveniente da Interactive Brokers
#
#
#-------------------------------------------------------------------------------------
import pandas as pd
df = pd.read_csv('trade2.csv')
print(df.to_string())
sums=df["Realized P&L"].sum()
print("profitto settimanale")
print(sums)
df2 =df.groupby(['Fin Instrument']).sum(["Realized P&L"])
print(df2)



new_df=df.assign(FinInstrument2=['Fin Instrument'])
print(new_df)