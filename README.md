# Trace Microbial Sequences & NGS Instruments

Research: To see if there is a relationship between the metadata and the contamination present in the resulting sequencing data.

# Python Environment

requirements.txt

Use at your Discretion. Provided as reference to reproduce working Environment. 

# Data

Assumption 1 : Public Study Accession ID name begins with "PRJ"
``` 
data
├── bam_files
|   ├── PRJ######
|       └──  <Run Accession>.bam
├── csv_files
|   ├── PRJ######
|       └── PRJ######_<Run Accession>.csv
├── sam_files
|   ├── PRJ######
|       └── <Run Accession>.sam
└── PRJ######
    ├── <Run Accession>_1.fastq
    └── <Run Accession>_2.fastq
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

#### Known Issues

Sometimes on dual read, the 2nd read will try to download twice ( does not affect storage)

## run_HISAT2.ipynb

#### Description

Notebook to process FASTQ files through HISAT2 to produce .sam files

#### Dependencies

[HISAT2](https://daehwankimlab.github.io/hisat2/)

[SAMTOOLS](https://www.htslib.org/)

[Genome Reference Consortium Human Build 38](https://genome-idx.s3.amazonaws.com/hisat/grch38_genome.tar.gz)

#### Inputs: 

Directory Path

FASTQ files in $PWD/< Public Study Accession ID >/< Run Accession >.fastq data structure

Note: Single Reads typically store as <Run Accession>.fastq while Dual reads will be stored as <Run Accession>_1.fastq and <Run Accession>_2.fastq

#### Outputs

SAM file in .sam format
Files are stored as $PWD/sam_files/< Public Study Accession ID >/<Run Accession>.sam data structure

#### Support 
[The Genome Reference Consortium](https://www.ncbi.nlm.nih.gov/grc)

## run_SAM_to_BAM.ipynb

#### Description

Notebook to Convert Sequence Alignment and Map (SAM) file to  Binary Alignment and Map (BAM) File. Additionally, will sort BAM file during conversion

#### Dependencies 

[SAMTOOLS](https://www.htslib.org/)

#### Inputs: 

$PWD/sam_files/< Public Study Accession ID >/<Run Accession>.sam data structure

#### Outputs

BAM file in .bam format
Files are stored as $PWD/bam_files/< Public Study Accession ID >/<Run Accession>.bam data structure

## run_etl_BAM_to_pd.ipynb

#### Description

Processing Pipeline

#### Dependencies 

capstoneUtils.py : Script containing additional processing functions

#### Inputs: 

Directory in structure $PWD/bam_files/< Public Study Accession ID >/<Run Accession>.bam data structure
Directory in structure $PWD/csv_files/< Public Study Accession ID >_<Run Accession>.csv data structure


#### Outputs

Run Directory structure


```
runs
└── K_< K >
    ├── images
    |   └── *.png
    ├── models
    |   └── lda_model_Ntopic< Number of Topics>_K<K>*
    ├── cluster_sample_K< K >.csv
    ├── crosstab_K< K >.csv
    ├── filtered_crosstab_K< K >.csv
    ├── K< K >_library.txt
    ├── kmer_df_K< K >.csv
    ├── objs_K< K >.pkl
    ├── sizes.csv
    ├── test.csv
    └── train.csv
```
##### File Descriptions 

- cluster_sample_K< K >.csv
    - 100000 Rows of K-Mer Length Sequences and Estimated Topic
- crosstab_K< K >.csv
    - Cross Tab in the Format K-Mer Length Sequence Rows and < Public Study Accession ID > Columns pre Chi-Squared Filtering 
- filtered_crosstab_K< K >.csv
    - Cross Tab in the Format K-Mer Length Sequence Rows and < Public Study Accession ID > Columns post Chi-Squared Filtering 
- K< K >_library.txt
    - List K-Mer Length Sequences derived from Training Set Post Chi-Squared Filtering 
- kmer_df_K< K >.csv
    - K-Mer Length Sequences derived from Training Set. Used to generate model
- objs_K< K >.pkl
    - Pickle file in format K, kmer_dictionary. kmer_dictionary format is: {< Public Study Accession ID and Run Accession> : K-Mer Length Sequences as List  }
- sizes.csv
    - File to show Raw Data number of Sequences and Pandas Data Frame Size. Useful to estimate RAM and Hard Disk Space Requirements 
- test.csv
    - Test Set of Sequences after initial import of Raw Data 
- train.csv
    - Training Set of Sequences after initial import of Raw Data  

# Optional Files

## run_chi_squared.ipynb
## run_classification.ipynb
## run_optimize.ipynb
