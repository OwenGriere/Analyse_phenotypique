# Presentation of the tool

This tool is about the constrcution of a Manhattan plot with large data. Those data are generated previously by using MORFEE and find all the ID's patient associate at all the genetics variants found through MORFEE in all gene of the human genome.

all the data are stock in the data folder, separated in chromosome and each txt file are formating like this :

    CHROM   POS             ID                      REF      ALT      ID patient
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

