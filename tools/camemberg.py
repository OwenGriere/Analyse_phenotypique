import pandas as pd
import argparse
import matplotlib.pyplot as plt
import seaborn as sns

parser = argparse.ArgumentParser()
parser.add_argument('txt_path', type=str, help="the txt path")
parser.add_argument('save_path', type=str, help="the save path")
args = parser.parse_args()


variants = pd.read_csv(args.txt_path, sep='\t', header=None)

chr = variants[0].tolist()
pos = variants[1].tolist()
ID = variants[2].tolist()
location = variants[5].tolist()
ORF = variants[4].tolist()

data = {
    'chr': chr,
    'pos': pos,
    'ID': ID,
    'location': location,
    'ORF': ORF
}
data=pd.DataFrame(data)
data = data[data['location'] == 'UTR5']

ensemble=set(ORF)
categorie=[]
valeur=[]
total=0
for i in ensemble:
    s=len(data[data['ORF'] == i])
    if s != 0:
        valeur.append(s)
        categorie.append(i)
        total+=s

df = {
    'Catégories': categorie,
    'Valeurs': valeur
}

df=pd.DataFrame(df)
print(df)

plt.figure(figsize=(12, 12))
wedges, texts, autotexts = plt.pie(df['Valeurs'], labels=df['Catégories'], autopct='%1.1f%%', startangle=140)

plt.legend(wedges, df['Catégories'], title="Type de Variations", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

plt.title(f"Distribution des types de variations pour les variants significatifs dans le 5'UTR pour {total} variants")
plt.savefig(f'{args.save_path}/Camemberg.png')