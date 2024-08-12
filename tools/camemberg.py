import pandas as pd # type: ignore
import argparse
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore

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
overlap = variants[6].tolist()

data = {
    'chr': chr,
    'pos': pos,
    'ID': ID,
    'location': location,
    'ORF': ORF,
    'overlap': overlap
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

test = data[data['ORF'] == 'uTIS']
overlapping = 0
not_overlapping = 0
elongated = 0


for i in range(len(data)):
    tab = data.iloc[i, 'overlap'].split()
    for j in tab:
        if j == "not_overlapping":
            not_overlapping+=1
        elif j == "elongated_CDS":
            elongated+=1
        else:
            overlapping+=1

overlapping ={
    'categories': ["overlapping","not_overlapping","elongated_CDS"],
    'valeurs': [overlapping,not_overlapping,elongated]
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 15))

wedges, texts, autotexts = ax1.pie(df['Valeurs'], labels=df['Catégories'], autopct='%1.1f%%', startangle=140)
ax1.legend(wedges, df['Catégories'], title="Type de Variations", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
ax1.set_title(f"Distribution des types de variations pour les variants significatifs dans le 5'UTR pour {total} variants")

wedges, texts, autotexts = ax2.pie(overlapping['valeurs'], labels=overlapping['catégories'], autopct='%1.1f%%', startangle=140)
ax2.legend(wedges, overlapping['catégories'], title="Conséquence sur la protéine produites", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
ax2.set_title(f"Distribution des conséquences pour les potéines induites par une mutation uTIS dans le 5'UTR")

plt.tight_layout()
plt.savefig(f'{args.save_path}/Camemberg.png')