#!/bin/bash

echo -e "\n\t\t\t\e[30;46m---------------\e[0m\n\t\t\t\e[30;46m--- WELCOME ---\e[0m\n\t\t\t\e[30;46m---------------\e[0m\n" 

printf "MODULE LOADING ... "
module load nextflow
source activate UTRAnnotator_env ## needed conda environment
source configuration/process.conf
echo -e "DONE\n"

mkdir -p $path/RESULT

nextflow run $path/tools/PROCESS.nf -c $configNF -with-report report.html ## nextflow parallelization by chromosome

printf "- Results Concatenation and Manhattan Plot ..."
awk '(NR == 1) || (FNR > 1)' $path/RESULT/*.csv > $path/df_analyse.csv ## concatenate all the csv in one
rm $path/RESULT/*.csv
mv $path/df_analyse.csv $path/RESULT/
python $path/tools/Plot.py $path/RESULT/df_analyse.csv $path/RESULT ## Plot Manhattan Plot
echo -e "DONE\n"

printf "- FILTERING MORFEE FILE ..." 
python $path/tools/FilterXLSX.py $MORFEE_tab $path/variants.txt $path/RESULT
echo -e "DONE\n"

printf "- Plotting Camembert ..."
python $path/tools/camemberg.py $path/variants.txt $path/RESULT
echo -e "DONE\n"

echo -e "\n\t\t\t\e[30;46m------------\e[0m\n\t\t\t\e[30;46m--- DONE ---\e[0m\n\t\t\t\e[30;46m------------\e[0m\n"
