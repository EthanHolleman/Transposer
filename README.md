

## Overview

This program is designed to allow researchers interested in LTR retrotransposons to quickly remap elements from outdated reference assembly versions to the latest version. 
The program is designed to be used with UNIX based operating systems, namely Mac and Linux flavors and was designed in Ubuntu.
Transposer was tested on datasets taken from *Glycine max* (modern soybean). This species was chosen as it is the primary focus of current research at the Laten Lab and it contains a wide array of LTR type transposable element families within its genome presenting many opportunities for remaps.

## Required Software / OS
Currently this program will only run on operating systems with a BASH terminal. The following programs just already be preinstalled.

* Bowtie 2
* Samtools
* Python 3

Transposer works best if you add the downloaded file to your path variables. It has not been tested on BASH programs for windows such as Putty. 

## Preliminary Quick Start Guide

* Preparing Refernce Assembly
   * Once required software is installed and added to your path variables clone the repository to your PC. If you already have LTR and complete element consensus sequences ready start by creating a new bowtie index using the -b parameter (coming soon) and providing a fasta file that will act as the reference assembly. This should be created using the most recent version of an organism's reference assembly. 

* Conducting Remap Searches
   * Call the remap.py script again and provide the LTR consensus, complete element consensus, and the name of the bowtie index you just created in the previous step using the -l, -s, and -i flags respectively. You may also want to change the allowance paramter which will change how the program recognizes solo LTRs. The default for this value is 150 base pairs of variance. The name of the family of elements you are remaping should also be provided using the -n flag in order to allow the program to properly name the maped elements. Finally, assuming sequences are taken from NCBI, provide the accession numbers file using the -k parameter.
   * If you wish to change the paramters of the actual bowtie search, the -a t flag can be used to edit the search.py file directly. Keep in mind currently this will alter the search parameters for both LTR searches and complete element searches. 

* Results
   * Results will be returned in a fasta file to standard output unless a location for the fasta file to be stored is given. This file will contain a complete list of ordered and named intact and solo elements found in both allignments. 
   
## How Transposer Works in Detail

### Initial Allignments
Transposer begins by aligning both the provided LTR and complete element consensus sequences of a particular LTR retrotransposon family against a Bowtie index generated from the most current reference assembly for a given organism. 
Transposer then uses samtools to sort and read in alignment data from both searches. 

### Finding Solo Elements
Transposer then takes the elements identified through the LTR consensus alignment and attempts to determine which pairs correspond to intact elements and which are solos. This is done by searching for pairs of LTRs exist within the length of the complete consensus from each other +- a degree of error which is specified using the -a (allowance) parameter. Truncated elements are treated as intact. 
Currently, if an element has nested within a member of its own family, Transposer will misinterpret this event and pair the closest LTRs together even if they originate from different elements. A solution to this problem will be coming later on. 

### Remaping and Renaming 
The last step Transposer will currently take is to rename all solo and intact elements identified by the consensus alignments based on their position in the queried reference. Results are returned in a fasta file.
Since the program is blind to the original names and locations of the elements in the previous reference, the new names will not correspond exactly to the previous convention if deletions or additions of elements have occurred between references. 
In a coming update Transposer will provide a map from old elements to new by matching flanking sequences in each reference. 
   
## Command Line Guide

| Flag     | Description          | Required? |
| ------------- |-------------| -----|
| -i     | Name of Bowtie 2 Index you wish to search against| True|
| -l      |Name of file containing the LTR consensus, currently must be .txt   |   True |
| -s | Name of file containing the complete element consensus, should include LTRs for best results, as currently must be .txt     |    True |
| -k | txt file containing the NCBI accession numbers and corresponding chromosome numbers. | True|
| -a | Allowance, set the number of base pair difference allowed between the length of the complete consensus and the distance of two LTRs for an `INTACT` classification, see the Finding Solos section for more info. If not given default is set ot 150 base pairs | False |
| -n | Name of element family you are remaping, if not specified will be set to NONE in the output file | False |
|-o | Name of output file that remaped elements will be written to in fasta format, if not given will be set to output.fasta | False
|-v | Verbose mode, transposer runs in quiet mode by defualt, setting verbose to "True" will enter verbose mode |False |
 
## Example Run

For this example run we will use the following files 
* Chr1GenBank -- Bowtie 2 index files of chromosome 1 of *Glycine max.* from NCBI GenBank
* GMR30Consensus.txt -- text file of complete consensus created from represenative group of GMR30 elements
* GMR30LTRConsensus.txt -- text file of consensus sequence of just the GMR30 LTRs
* accessionNums.txt -- file from NCBI containing translation of accession numbers to chromosome numbers

Since the Bowtie index is already built we can issue the command below
```
remap.py -i Chr1GenBank -s GMR30LTRConsensus.txt -l GMR30Consensus.txt -k accessionNums.txt -a 200 -o testRun.fasta
```

In this run we have also specified the optional parameters -a to 200 to increase the allowance in detecting solo elements and -o to set the output file. 

`Include results of run with explaination next`
