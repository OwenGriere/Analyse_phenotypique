#!/usr/bin/env nextflow

params.directory = '/home/ogriere/scratch/5_prime_UTR/DO_NOT_TOUCH'

workflow {
    canal=Channel.fromPath("${params.directory}/data/*.txt")
                 .map{PATH -> [PATH, file(PATH).getBaseName()]}
    Analyse_pheno(canal)
}

// Parallelization of all different txt tab (in our case each txt tab is for one chromosome in particular)

process Analyse_pheno {
tag "Analyse of ${name}"

    input:
    tuple val(path), val(name)

    output:

    script:
    """
    python ${params.directory}/tools/analyse.py ${path} '${params.directory}/RESULT' '${params.directory}/data/pheno_full.tsv' ${name}
    """
}