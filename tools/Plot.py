import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import argparse

## Arguments for the python script
parser = argparse.ArgumentParser()
parser.add_argument('tab_path', type=str, help="the save path")
parser.add_argument('save_path', type=str, help="the save path")
args = parser.parse_args()

######################################################################################################################
################################################# Graphics ###########################################################
######################################################################################################################

## load the concatenated csv file
df_analyse = pd.read_csv(args.tab_path)

## generate a a color palette for all chromosome
colors = sns.color_palette("husl", df_analyse['chr'].nunique())

## define the threshold
threshold=-np.log10(0.05/len(df_analyse))
chromosomes = df_analyse['chr'].unique()
chromosome_offsets = {}
current_offset = 0


## filter all the significants variants
result = df_analyse[df_analyse['p-value'] <= 0.05/len(df_analyse)]
result = result[['chr','pos','ID','-log10(p-value)']]

## separate the chromosome on the plot

for chrom in sorted(chromosomes):
    chrom_length = df_analyse[df_analyse['chr'] == chrom]['pos'].max()
    chromosome_offsets[chrom] = current_offset
    current_offset += chrom_length #+ 1000000

df_analyse['adjusted_pos'] = df_analyse.apply(lambda row: row['pos'] + chromosome_offsets[row['chr']], axis=1)

## generate the plot
plt.figure(figsize=(25, 12))
sns.scatterplot(data=df_analyse, x='adjusted_pos', y='-log10(p-value)', hue='chr', palette=colors, legend='full', s=30, alpha=0.7)

plt.axhline(y=threshold, color='red', linestyle='--')
plt.text(x=chromosome_offsets[sorted(chromosomes)[-1]] / 8, y=threshold + 0.2, s=f"Limite de significativité à {threshold}, {len(result)} variants significatifs", color='red', ha='center')

for chrom in sorted(chromosomes):
    plt.axvline(x=chromosome_offsets[chrom], color='gray', linestyle='--')

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
        center = chromosome_offsets[chrom] + (current_offset - chromosome_offsets[chrom]) / 2
    chromosome_centers[chrom] = center
plt.xticks(list(chromosome_centers.values()), list(chromosome_centers.keys()))

plt.legend(title='Chromosome')


## Save the plot and the txt file

plt.savefig(f'{args.save_path}/Manhattan.png')

#result.to_csv(f'{args.save_path}/result.txt',sep='\t', index=False, float_format='%.2e', line_terminator='\n')
with open(f'{args.save_path}/variants.txt', 'w') as file:
    for index, row in result.iterrows():
        file.write('\t'.join(map(str, row.values)) + '\n')
