#!/bin/bash
#$ -S /bin/bash
#$ -M owen.griere@etu.u-paris.fr
#$ -m abe
#$ -cwd
#$ -q max-24h.q

module load nextflow
source activate UTRAnnotator_env ## needed conda environment
source configuration/process.conf

echo -e "\n\t\t\t--- WELCOME ---\n" 
mkdir -p $path/RESULT

nextflow run $path/tools/PROCESS.nf -c $configNF -with-report report.html

awk '(NR == 1) || (FNR > 1)' $path/RESULT/*.csv > $path/df_analyse.csv

python $path/tools/Plot.py $path/df_analyse.csv $path

echo -e "\t\t\t--- DONE ---" 
