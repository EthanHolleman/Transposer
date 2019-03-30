

## Overview

This program is designed to allow researchers interested in transposable elements to quickly remap elements from outdated reference assembly versions to the latest version.
The program is designed to be used with UNIX based operating systems, namely Max and Linux flavors and was designed in Ubuntu.
The program was tested on datasets taken from *Glycine max* (modern soybean). This species was chosen as it is the primary focus of current research at the Laten Lab and it contains a high degree of transposable elements within its genome presenting many opportunities for remaps.

## Required Software / OS
Currently this program will only run on operating systems with a BASH terminal. The following programs just already be preinstalled.

* Bowtie 2
* Samtools
* Python 3

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
