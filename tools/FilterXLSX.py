import pandas as pd #type: ignore
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('XLSX_path', type=str, help="the MORFEE path")
parser.add_argument('txt_path', type=str, help="the txt path")
parser.add_argument('save_path', type=str, help="the save path")
args = parser.parse_args()


# Lire le fichier Excel
MORFEE = pd.read_excel(args.XLSX_path, sheet_name='Sheet1')

variants = pd.read_csv(args.txt_path, sep='\t', header=None)

gene_columns = MORFEE.filter(regex=r'^Gene\.').columns.tolist()
columns_to_select = ['seqnames', 'start','REF','ALT','avsnp150']  + gene_columns +['Transcript','RefSeq_transcript'
                    ,'Func.ensGene','orfSNVs_type','TIS_sequence','modification_type','orfSNVs_frame'
                    ,'type_of_generated_ORF','NewAALength','Kozak_sequence','Kozak_score'
                    ,'gwasCatalog','CLNDN','CLNDISDB','CLNSIG']
MORFEE = MORFEE[columns_to_select].copy()


chr = variants[0].tolist()
pos = variants[1].tolist()
ID = variants[2].tolist()

ORF_type=[]
location=[]
overlap=[]
dataframes=[]

for i in range(len(ID)):
    line=MORFEE[(MORFEE['seqnames'] == chr[i]) & (MORFEE['start'] == pos[i])]
    dataframes.append(line)
    ORF_type.append(line['orfSNVs_type'].values[0] if not line['orfSNVs_type'].empty else 'NA')
    location.append(line['Func.ensGene'].values[0] if not line['Func.ensGene'].empty else 'NA')
    temp=[]
    for i in line['type_of_generated_ORF'].values[0].split(';'):
        temp.append(i)
    overlap.append(' '.join(temp))
df_result = pd.concat(dataframes, ignore_index=True)

output_file = f'{args.save_path}/filtered_MORFEE.xlsx'
df_result.to_excel(output_file, index=False)
df_result[df_result['Func.ensGene']=='UTR5'].to_excel(f'{args.save_path}/UTR5_MORFEE.xlsx',index= False)

print(df_result.head(10))
print(f"On trouve {len(df_result)} issue de MORFEE dont {len(df_result[df_result['Func.ensGene']=='UTR5'])} en particulier dans le 5'UTR")

with open(args.txt_path, 'r') as file:
    lines = file.readlines()

modified_lines = [line.rstrip('\n') + f'\t{ORF_type[index]}\t{location[index]}\t{overlap[index]}' + '\n' for index,line in enumerate(lines)]

with open(args.txt_path, 'w') as file:
    file.writelines(modified_lines)
