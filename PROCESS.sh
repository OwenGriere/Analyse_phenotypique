#!/bin/bash

echo -e "\n\t\t\t\e[30;46m---------------\n\t\t\t--- WELCOME ---\n\t\t\t---------------\e[0m\n" 

printf "MODULE LOADING ... "
module load nextflow
source activate UTRAnnotator_env ## needed conda environment
source configuration/process.conf
echo -e "DONE\n"

mkdir -p $path/RESULT

nextflow run $path/tools/PROCESS.nf -c $configNF -with-report report.html ## nextflow parallelization by chromosome

awk '(NR == 1) || (FNR > 1)' $path/RESULT/*.csv > $path/df_analyse.csv ## concatenate all the csv in one

python $path/tools/Plot.py $path/df_analyse.csv $path ## Plot Manhattan Plot

echo -e "\t\t\t--- DONE ---" 

echo -e "FILTERING MORFEE FILE ..."

