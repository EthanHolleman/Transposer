

## Overview

This program is designed to allow researchers interested in transposable elements to quickly remap elements from outdated reference assembly versions to the latest version.
The program is designed to be used with UNIX based operating systems, namely Max and Linux flavors and was designed in Ubuntu.
The program was tested on datasets taken from *Glycine max* (modern soybean). This species was chosen as it is the primary focus of current research at the Laten Lab and it contains a high degree of transposable elements within its genome presenting many opportunities for remaps.

## Required Software / OS
Currently this program will only run on operating systems with a BASH terminal. The following programs just already be preinstalled.

* Bowtie 2
* Samtools
* Python 3

## Preliminary Quick Start Guide

* Preparing Refernce Assembly
   * Once required software is installed and added to your path variables clone the repository to your PC. If you already have LTR and complete element consensus sequences ready start by creating a new bowtie index using the -b parameter and providing a fasta file that will act as the reference assembly.

* Conducting Remap Searches
   * Call the remap script again and provide the LTR consensus, complete element consensus, and the name of the bowtie index you just created in the previous step using the -l, -s, and -i flags respectively. You may also want to change the allowance paramter which will change how the program recognizes solo LTRs. The default for this value is 500 base pairs. The name of the family of elements you are remaping should also be provided using the -n flag in order to allow the program to properly name the maped elements.
   * If you wish to change the paramters of the actual bowtie search, the -a t flag can be used to edit the search.py file directly. Keep in mind currently this will alter the search parameters for both LTR searches and complete element searches. 

* Results
   * Results will be returned in a fasta file to standard output unless a location for the fasta file to be stored is given. This file will contain a complete list of ordered and named intact and solo elements found in both allignments. 
   



## Future Sections to Include
* Quick start guide 
* Method for detecting solo vs intact elements
* Method for handeling truncated elements
* Potnetial issues section
    * nested elements of the same family 
 

## Current File Structure 
The program will be divided into two main scripts that can act independently. The primary funcionality of the program will come from the remap.py file which acts as the main method for remaping LTR elements using Bowtie2. This program requires consensus sequecnes of both the LTR and element sequences. 
If you do not have these already they can be generated from a fasta file using the con.py file which will act as a python interface to the pertient PAGAN functionality. 


```
.
├── consensus
│   ├── argsCon.py
│   ├── con.py
│   └── pagan
│       └── bin
│           ├── bppancestor
│           ├── bppdist
│           ├── bppphysamp
│           ├── exonerate
│           ├── lib
│           │   ├── disttbfast
│           │   ├── libglib-2.0.so.0
│           │   ├── tbfast
│           │   └── version
│           ├── mafft
│           ├── pagan
│           └── raxml
├── __pycache__
│   ├── args.cpython-37.pyc
│   ├── element.cpython-37.pyc
│   └── interp.cpython-37.pyc
├── README.md
└── remap
    ├── argsRemap.py
    ├── chr2.sorted.bam.txt
    ├── element.py
    ├── __init__.py
    ├── interp.py
    ├── __pycache__
    │   ├── argsRemap.cpython-37.pyc
    │   ├── element.cpython-37.pyc
    │   └── interp.cpython-37.pyc
    ├── remap.py
    └── tier.py


```
File structure is likely to change as I figure out a better layout. Probably should include a bin file or something like that
