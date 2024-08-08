import pandas as pd
import argparse
from sklearn.preprocessing import StandardScaler
import random
import numpy as np
from scipy import stats


parser = argparse.ArgumentParser()

parser.add_argument('path', type=str, help="the path for the txt")
parser.add_argument('save_path', type=str, help="the save path")
parser.add_argument("pathTab", type=str, help='path tab pheno')
parser.add_argument("name", type=str, help='name of the txt file')
args = parser.parse_args()


def normalize_group(group):
    scaler = StandardScaler()
    # Reshape et normalisation des colonnes spécifiées
    group[cols_to_normalize] = scaler.fit_transform(group[cols_to_normalize])
    return group

######################################################################################################################
################################################# Read Phenotype Data ################################################
######################################################################################################################

df_pheno = pd.read_csv(args.pathTab, sep='\t')
df_pheno = df_pheno.set_index('ID')

df_pheno = df_pheno.loc[:, ['Age','Sex', 'LDL','Cholesterol_lowering_medication']]
df_pheno = df_pheno.dropna(subset=['Age','Sex', 'LDL','Cholesterol_lowering_medication'])

df_pheno['Cholesterol_lowering_medication'] = df_pheno['Cholesterol_lowering_medication'].map({'yes': 1, 'no': 0})
scaler = StandardScaler()
cols_to_normalize = ['LDL']

df_pheno = df_pheno.groupby(['Age', 'Sex', 'Cholesterol_lowering_medication'], group_keys=False).apply(normalize_group)

######################################################################################################################
################################################# Generate pandas ####################################################
######################################################################################################################

df_analyse = {
    'chr': [],
    'pos': [],
    'ID': [],
    'patients': [],
    'p-value': []
}

df_patients = {
    'ID': [],
    'variants':[],
    'LDL': []
}

"""
pattern = os.path.join(args.path, '*.txt')
fichiers_texte = glob.glob(pattern)
"""

with open(args.path, 'r' ) as file:
    for line in file:
        element = line.strip().split('\t')
        df_analyse['chr'].append(element[0])
        df_analyse['pos'].append(element[1])
        df_analyse['ID'].append(element[2])
        df_analyse['p-value'].append(0.0)

        patient_list=element[5].split()
        df_analyse['patients'].append(patient_list)

        for id in patient_list:

            if int(id) in df_pheno.index:
                df_patients['ID'].append(int(id))
                df_patients['variants'].append(element[2])
                df_patients['LDL'].append(df_pheno["LDL"].loc[int(id)])


df_analyse=pd.DataFrame(df_analyse)
df_patients=pd.DataFrame(df_patients)
df_patients.set_index('variants', inplace=True)

######################################################################################################################
################################################# Statistiques #######################################################
######################################################################################################################

echantillon_global = df_pheno[~df_pheno.index.isin(df_patients['ID'])]['LDL']

variants_np = df_patients.index.to_numpy()
ldl_np = df_patients['LDL'].to_numpy()

for index, row in df_analyse.iterrows():
    
    echantillon_a_tester = ldl_np[variants_np == row['ID']].tolist()
    #echantillon_a_tester = df_patients.loc[row['ID'], 'LDL'].tolist()
    if isinstance(echantillon_a_tester, float):
        echantillon_a_tester = [echantillon_a_tester]
    
    if len(echantillon_a_tester)==0:
        df_analyse.drop(index)

    else:
        df_analyse.at[index, 'p-value'] = stats.ttest_ind(echantillon_a_tester, echantillon_global)[1]
        if row['p-value'] == 0:
            df_analyse.drop(index)

df_analyse['-log10(p-value)'] = -np.log10(df_analyse['p-value'])

df_analyse.to_csv(f'{args.save_path}/{args.name}.csv', index=False, float_format='%.2e')

#print(f"\nTableau des variants isolé par MORFEE de taille : {df_analyse.shape}\n{df_analyse.head(20)}")
