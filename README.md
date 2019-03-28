# Transposer

## Overview

This program is designed to allow researchers interested in transposable elements to quickly remap elements from outdated reference assembly versions to the latest version.
The program is designed to be used with UNIX based operating systems, namely Max and Linux flavors and was designed in Ubuntu.
The program was tested on datasets taken from *Glycine max* (modern soybean). This species was chosen as it is the primary focus of current research at the Laten Lab and it contains a high degree of transposable elements within its genome presenting many opportunities for remaps.

## Required Software
In order to use this program you must have already installed the following programs

* Bowtie 2
* Samtools
* Python 3

## Current File Structure

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
    ├── element.py
    ├── __init__.py
    ├── interp.py
    ├── remap.py
    └── tier.py
