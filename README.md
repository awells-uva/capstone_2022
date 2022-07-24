# Trace Microbial Sequences & NGS Instruments

# Data

``` 
data
|--bam_files
|  |--PRJ######
|  |  |--*.bam
|--csv_files
|  |--PRJ######
|  |  |--*.csv
|--sam_files
|  |--PRJ######
|  |  |--*.sam
|--PRJ######
|  |--*.fastq
```
# Scripts

## run_download_data.ipynb


#### Description

Notebook to download [FASTQ](https://support.illumina.com/bulletins/2016/04/fastq-files-explained.html) Files from [The European Nucleotide Archive (ENA)](https://www.ebi.ac.uk/ena/portal)

#### Dependencies 

#### Inputs

Public Study Accession ID ( Typically in Form PRJ##### )

#### Outputs

FASTQ files Unpacked into $PWD/< Public Study Accession ID >/*.fastq

## run_HISAT2.ipynb

#### Description

#### Dependencies

[HISAT2](http://daehwankimlab.github.io/hisat2/)

[Genome Reference Consortium Human Build 38](https://genome-idx.s3.amazonaws.com/hisat/grch38_genome.tar.gz)

#### Inputs: 

#### Outputs

#### Support 
[The Genome Reference Consortium](https://www.ncbi.nlm.nih.gov/grc)

## run_SAM_to_BAM.ipynb

#### Description

#### Dependencies 

#### Inputs: 

#### Outputs

## run_etl_BAM_to_pd.ipynb

#### Description

#### Dependencies 

capstoneUtils.py


#### Inputs: 

#### Outputs



# Optional Files

## run_chi_squared.ipynb
## run_classification.ipynb
## run_optimize.ipynb
