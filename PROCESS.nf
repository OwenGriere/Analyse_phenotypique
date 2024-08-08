#!/usr/bin/env nextflow

params.directory = '/home/ogriere/scratch/5_prime_UTR/DO_NOT_TOUCH'

workflow {
    canal=Channel.fromPath("${params.directory}/data/*.txt")
                 .map{PATH -> [PATH, file(PATH).getBaseName()]}
    Analyse_pheno(canal)
}

process Analyse_pheno {
tag "Analyse of ${name}"

    input:
    tuple val(path), val(name)

    output:

    script:
    """
    python ${params.directory}/tools/analyse.py ${path} ${params.directory} '/home/ogriere/scratch/5_prime_UTR/pheno_full.tsv' ${name}
    """
}