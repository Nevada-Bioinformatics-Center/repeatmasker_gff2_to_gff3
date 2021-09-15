# repeatmasker_gff2_to_gff3

This is a simple python script to convert RepeatMasker output files from GFF2 format to GFF3, and include repeat_class annotation information


## Authors

* Hans Vasquez-Gross (@hansvg)

## Usage

### Simple

#### Step 1: clone repository

clone this repo to your local computer

#### Step 2: run the python script

The necessary options are --gff2 with the RepeatMasker  *.gff output and
the table file from RepeatMasker named "*.ori.out"

Example run:

`python repeatmasker_gff2_to_gff3.py --gff2 Csc24Chr.fasta.out.gff Csc24Chr.fasta.ori.out --o test.gff3`


