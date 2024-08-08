import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('tab_path', type=str, help="the save path")
parser.add_argument('save_path', type=str, help="the save path")
args = parser.parse_args()

######################################################################################################################
################################################# Graphiques #########################################################
######################################################################################################################
df_analyse = pd.read_csv(args.tab_path)

colors = sns.color_palette("husl", df_analyse['chr'].nunique())

threshold=-np.log10(0.05/len(df_analyse))
chromosomes = df_analyse['chr'].unique()
chromosome_offsets = {}
current_offset = 0

result = df_analyse[(df_analyse['p-value'] <= 0.05/len(df_analyse)) & (df_analyse['p-value'] > 0)]

for chrom in sorted(chromosomes):
    chrom_length = df_analyse[df_analyse['chr'] == chrom]['pos'].max()
    chromosome_offsets[chrom] = current_offset
    current_offset += chrom_length #+ 1000000

df_analyse['adjusted_pos'] = df_analyse.apply(lambda row: row['pos'] + chromosome_offsets[row['chr']], axis=1)

plt.figure(figsize=(25, 12))
sns.scatterplot(data=df_analyse, x='adjusted_pos', y='-log10(p-value)', hue='chr', palette=colors, legend='full', s=30, alpha=0.7)

plt.axhline(y=threshold, color='red', linestyle='--')
plt.text(x=chromosome_offsets[sorted(chromosomes)[-1]] / 2, y=threshold + 0.2, s=f"Limite de significativité, {len(result)} variants sont trouvés", color='red', ha='center')

for chrom in sorted(chromosomes):
    plt.axvline(x=chromosome_offsets[chrom], color='gray', linestyle='--')

# Ajout de labels et de titre
plt.xlabel('Position chromosomique')
plt.ylabel('p-value logscale')
plt.title('Manhattan Plot des variants exomiques')
          
chromosome_centers = {}
sorted_chromosomes = sorted(chromosomes)
for i, chrom in enumerate(sorted_chromosomes):
    if i < len(sorted_chromosomes) - 1:
        next_chrom = sorted_chromosomes[i + 1]
        center = (chromosome_offsets[chrom] + chromosome_offsets[next_chrom]) / 2
    else:
        # Pour le dernier chromosome, utiliser la fin de la dernière section
        center = chromosome_offsets[chrom] + (current_offset - chromosome_offsets[chrom]) / 2
    chromosome_centers[chrom] = center
plt.xticks(list(chromosome_centers.values()), list(chromosome_centers.keys()))

# Affichage de la légende
plt.legend(title='Chromosome')
plt.savefig(f'{args.save_path}/Manhattan.png')


result.to_csv(f'{args.save_path}/result.csv', index=False, float_format='%.2e')

