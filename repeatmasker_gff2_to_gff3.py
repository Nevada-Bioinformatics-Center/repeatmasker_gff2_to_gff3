#!/usr/bin/env python

"""
A simple python script to convert RepeatMasker output files from
GFF2 format to GFF3, and include repeat_class annotation information
GITHUB Repo: https://github.com/Nevada-Bioinformatics-Center/repeatmasker_gff2_to_gff3
"""

import sys
import argparse
import re
from datetime import datetime

EXIT_FAILURE = 1
EXIT_SUCCESS = 0
now = datetime.now() # current date and time


def main(arguments):

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('tablefile', help="Input *.ori.out file from RepeatMasker (looks like a table)", type=argparse.FileType('r'))
    parser.add_argument('-g', '--gff2', help="Input GFF2 file", type=argparse.FileType('r'))
    parser.add_argument('-o', '--outfile', help="Output file", default=sys.stdout, type=argparse.FileType('w'))
    args = parser.parse_args(arguments)


    if not args.tablefile:
        parser.print_usage()
        return sys.exit(EXIT_FAILURE)

    dataDict = dict()
    
    print("Reading *.ori.out file from RepeatMasker", file=sys.stderr)
    with args.tablefile as f:
        for line in f:
            lineArr = line.split()
            contig = lineArr[4]
            start = lineArr[5]
            end = lineArr[6]
            name = lineArr[9]
            family = lineArr[10]
            if name not in dataDict:
                dataDict[name] = family
            else:
                if dataDict[name] != family:
                    print("Class does not match already assigned class to repeat name")
                    return sys.exit(EXIT_FAILURE)


    if not args.gff2:
        parser.print_usage()
        return sys.exit(EXIT_FAILURE)

#example GFF2 line from repeatmasker
#Chr01   RepeatMasker    similarity      14      154     22.0    -       .       Target "Motif:rnd-6_family-12" 684 821
    #pattern = "Motif:([\w-]+)"

    print("Reading gff2 file from RepeatMasker", file=sys.stderr)
    repeat_num = 0
    pattern = "Motif:(.+)\""
    with args.outfile as o:
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        o.write("##gff-version 3\n")
        o.write("##Generated using repeatmasker_gff2_to_gff3.py on %s\n" % date_time)
        o.write("##repeatmasker_gff2_to_gff3.py can be found at URL: https://github.com/Nevada-Bioinformatics-Center/repeatmasker_gff2_to_gff3 \n")
        with args.gff2 as f:
            for line in f:
                if "#" not in line:
                    repeat_num += 1
                    (contig, source, method, start, end, score, strand, phase, info) = line.split("\t")

                    if match := re.search(pattern, info):
                        matchtext = match.group(1)
                    else:
                        print("Could not find repeat_name in last column of GFF2, exiting", file=sys.stderr)
                        return sys.exit(EXIT_FAILURE)

                    if "rich" not in matchtext:
                        repeat_class = dataDict[matchtext]
                    else:
                        repeat_class = matchtext

                    new_group = "ID=TE.%s.csc.repeat%09d;Name=TE.%s.csc.repeat%09d;repeat_match=%s;repeat_class=%s;" %  (contig, repeat_num, 
                        contig, repeat_num, matchtext, repeat_class.replace("/", "%2F"))

                    o.write("\t".join([contig,source,"repeat_region",start,end,score,strand,phase,new_group]) + "\n")

       
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
        
