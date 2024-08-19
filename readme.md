# Presentation of the tool

This tool is about the constrcution of a Manhattan plot with large data. Those data are generated previously by using MORFEE and find all the ID's patient associate at all the genetics variants found through MORFEE in all gene of the human genome.

this tools are made to be used on a cluster as the BiRD cluster.

all the data are stocked in the data folder, separated in chromosome and each txt file are formating like this :

    CHROM   POS             ID                      REF     ALT     ID patient
    chr22	18527977	chr22_18527977_G_A	G	A	2370776 2386621

the column ID patient contains all the ID associated at a variant in particular and separated by a space

There is also a phenotype table where ID patient are associate at several phenotypes like LDL or Age.

# How to make it works 

First of all, you need to have python 3.0 or more on your computer with the following libraries :

    - matplotlib
    - seaborn
    - pandas
    - numpy
    - argparse
    - sklearn
    - scipy

You need to also have nextflow on the cluster

# Architecture of the tool

## Example folder

Contains the manhattan plot obtain when you execute the tools with the files currently present in the data folder 

## data folder

Contains data of several chromosome to test the tool and a table of phenotypes

## tools folder

- analyse.py which generate the csv usefull for the creation of the Manhattan plot and calculate also the p-value of a Student test for all variants

- Plot.py use the concatanated csv to plot the Manhattan plot and return an other txt with only the signifiant variants

- PROCESS.nf is a nextflow script which parallelizes the execution by the differents files in our case : 4 parallelizations but 22 in a full human genome (without XY)

- camemberg.py return a camembert plot showing the distribution of type of generated ORF for uTIS and type of variation for variants in UTR 5'

## configuration folder 

Contains 2 configuration files :

- analyse.config is the nextflow config file which needed the working directory for the execution (is this directory you must have a data folder with the txt data)
- process.conf is the PROCESS.sh config file. it contains the working directory (same of previously), the path for the nextflow config file and the path for the MORFEE tab 

## PROCESS.sh

it's the heart of the tool, when you had install the tool on your computer you just need to execute these commands :

    chmod u+x PROCESS.sh
    ./PROCESS.sh