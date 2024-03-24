import pandas
import matplotlib.pyplot as plt
import seaborn as sns 
import os


data_path = os.path.dirname(os.path.abspath(__file__))+'/data'
import zipfile
with zipfile.ZipFile(data_path+'/comptage_velo_2023.csv.zip', 'r') as zip_ref:
    zip_ref.extractall(data_path)

csv_filepath = data_path + '/comptage_velo_2023.csv'
print('filepath: '+ csv_filepath)
df = pandas.read_csv(csv_filepath)
df["datetime"] = pandas.to_datetime(df["date"]+" "+df["heure"])
#df["delta"] = pandas.to_timedelta(df["heure"])
#df['day_of_year'] = pandas.to_datetime(df['date']).dt.day_of_year
print(df.info())

# Somme de passage par compteur
#a = df.groupby(['latitude','longitude','id_compteur'])['nb_passages'].agg('sum')
#print(a)

#Max (coin Rosemont/St-Laurent)
# DF1 ID=100003032
df1 = df[(df['id_compteur'] == 100003032)]
# Ajout Mv Average
df1['semaine_mv'] = df1['nb_passages'].rolling(672).mean()
print(df1.dtypes)
# DF2 ID=100003032 - Groupement par date
df2 = df1.groupby(['date'])['nb_passages'].agg('sum')
print(df2)

df1.plot(x='datetime', y='semaine_mv', c = 'red')
plt.show()

matrix = df1.pivot_table(index="heure", columns="date", values="nb_passages")
sns.heatmap(matrix)
plt.show()
