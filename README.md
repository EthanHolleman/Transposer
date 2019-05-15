

## Overview

This program is designed to allow researchers interested in LTR retrotransposons to quickly remap elements from outdated reference assembly versions to the latest version. 
The program is designed to be used with UNIX based operating systems, namely Mac and Linux flavors and was designed in Ubuntu.
Transposer was tested on datasets taken from *Glycine max* (modern soybean). This species was chosen as it is the primary focus of current research at the Laten Lab and it contains a wide array of LTR type transposable element families within its genome presenting many opportunities for remaps.

## Required Software / OS
Currently this program will only run on operating systems with a BASH terminal. The following programs just already be preinstalled.

* Bowtie 2
* BLAST+
* Samtools
* Python 3

Transposer works best if you add the downloaded file to your path variables. It has not been tested on BASH programs for windows such as Putty. 

##Quick Start Guide

* What you need
	* Outdated and current assembly sequence files
	* List of outdated LTR retrotransposons in [this format](https://soybase.org/soytedb/te_request.php?class=I&subclass=I&order=LTR&superfam=Gypsy&fam=Gmr30)
	* Consensus sequences of LTR and complete element created from members of the family you intend to remap
	* 
  * GenBank Accession files for both assemblies
 Next follow these steps 
 
 1. Create BLAST nucleotide databases for both assembly versions
 ```
 buildblastdb -in <assembly file> -dbtype <nucl> -out <exampleDB>
 ```
 2. Create Bowtie 2 index of current assembly
 ```
 bowtie2-build -f <current Assembly> <index name>
 ```
 3. Run command with appropriate variable names
 ```
 remap.py -i <Bowtie_Index> -s <LTR_Consensus> -l <Element_Consensus> -k <Current_assembly_accession> -a 50 -o <output_File> -name <Element_Family_name> -c <Current_assembly_BLASTdb> -p <Outdated_assembly_BLASTdb> -m <Outdated_assebmly_accession> -e <Outdated_Elements>
 ```
 ## Command Line Guide

| Flag     | Description          | Required? |
| ------------- |-------------| -----|
| -i            | Name of Bowtie 2 Index you wish to search against| True|
| -l      |Name of file containing the LTR consensus, currently must be .txt   |   True |
| -s | Name of file containing the complete element consensus, should include LTRs for best results, as currently must be .txt     | True |
| -k | GenBank accession numbers and corresponding chromosome numbers, current assembly. | True |
 -m | GenBank accession numbers and corresponding chromosome numbers, outdated assembly | True 
 -c | BLAST database of current assembly | True 
 -p | BLAST database of previous assembly | True 
| -e | List of previous, outdated elements | True |
| -a | Allowance, set the number of base pair difference allowed between the length of the complete consensus and the distance of two LTRs for an `INTACT` classification, see the Finding Solos section for more info. If not given default is set ot 150 base pairs | False |
| -n | Name of element family you are remaping, if not specified will be set to NONE in the output file | False |
|-o | Name of output file that remaped elements will be written to in fasta format, if not given will be set to output.fasta | False
|-v | Verbose mode, transposer runs in quiet mode by defualt, setting verbose to "True" will enter verbose mode |False |
 
## Output 

Running remap.py will return a fasta file containing the collection of remaped elements ordered based on their locations in their respective chromosomes, as is shown in the example output below. Top lines can be read as element name, start location, end location, length, status (Intact or solo). 

```
>GMR30 1-1,3469733,3482833,13100,INTACT
TGTTTACGCTGGAATTTGGTAAACAACCGCTAGTCTAAGTTAATTGCT...
>GMR30 1-2,37210498,37223598,13100,INTACT
TGTTTACGCTGGAATTTGGTAAACAACCGCTAGTCTAAGTTAATTGCT...
>GMR30 1-3,38119449,38132549,13100,INTACT
TGTTTACGCTGGAATTTGGTAAACAACCGCTAGTCTAAGTTAATTGCT...
>GMR30 1-4,50123892,50124736,844,SOLO
TGTTAGCCCATATTTTTGATGAGATAAAAATATGCTCTAAATACGAAT...
```

The run will also return a matchReport.txt which contains the results of the backmap functionality. Elements found in the same rows of this file are likely to be the same element across the reference versions. 
```
GMR30 1-2	Gm1-2
CM000834.3	CM000834.1
INTACT		INTACT
37210498	35844653
37223600	35857770
13103		13117
```

## Example Results 

Results of complete GMR30 remap compared to the original 2010 assembly element locations 
![comparePlot](https://user-images.githubusercontent.com/45807040/57342019-4d2a4580-7102-11e9-9e23-7ee95f2fa867.png)
