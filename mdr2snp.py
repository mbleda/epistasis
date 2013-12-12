#!/usr/bin/python

__author__ = 'mbleda'

import sys, getopt
import re
import operator

vcfFile = ''
mdrFile = ''
outSnpFile = ''
outFile = ''

## Read arguments
#==========================================================
def main():
    global vcfFile
    global mdrFile
    global outFile
    global outSnpFile
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hv:m:s:o:", ["vcffile=","mdrfile=","outsnpfile=","outfile="])
    except getopt.GetoptError as err:
        ## print help information and exit
        print (str(err))
        print ('USAGE: mdr2snp.py -v <vcfFile> -m <mdrFile> -s <outSnpFile> -o <outFile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print ('mdr2snp.py -v <vcfFile> -m <mdrFile> -s <outSnpFile> -o <outFile>')
            sys.exit()
        elif opt in ("-v", "--vcffile"):
            vcfFile = arg
        elif opt in ("-m", "--mdrfile"):
            mdrFile = arg
        elif opt in ("-s", "--outsnpfile"):
            outSnpFile = arg
        elif opt in ("-o", "--outfile"):
            outFile = arg


if __name__ == "__main__":
    main()
#==========================================================

## Read VCF file to get the correspondence between the snp and the line
#==========================================================
line2snp = {}
lineNum = 1

vcf= open(vcfFile, "r").readlines()

print ("Obtaining correspondences SNP --> VCF line...")
for vcfLine in vcf:
    if not vcfLine.startswith("#"):
        vcfFields = vcfLine[0:-1].split("\t")
        if str(lineNum) not in line2snp:
            line2snp[str(lineNum)] = vcfFields[2]
        lineNum += 1

## Read MDR file and change line numbers into SNP ids
#==========================================================
mdr= open(mdrFile, "r").readlines()
out = open(outFile, "w")

snpList = {}

print ("Translating line numbers into SNP ids...")
for mdrLine in mdr:
    if not mdrLine.startswith("#"):
        mdrLineFormatted = re.findall(r"[^\s,]+", mdrLine)
        arrSize = len(mdrLineFormatted)
        print >> out, "%s\t( %s , %s )\t%s" %(mdrLineFormatted[0], line2snp[mdrLineFormatted[2]], line2snp[mdrLineFormatted[3]], "\t".join(mdrLineFormatted[6:arrSize]))
        ## Generate SNP list
        if not line2snp[mdrLineFormatted[2]] in snpList:
            snpList[line2snp[mdrLineFormatted[2]]] = mdrLineFormatted[arrSize-1]
        if not line2snp[mdrLineFormatted[3]] in snpList:
            snpList[line2snp[mdrLineFormatted[3]]] = mdrLineFormatted[arrSize-1]
    else:
        print >> out, "%s" %(mdrLine.rstrip())
out.close()

## Create ranked SNP list file (optional)
#==========================================================
if outSnpFile != '':
    sortedSnpList = sorted(snpList.items(), key=lambda t: t[1], reverse=True)

    outSnp = open(outSnpFile, "w")
    for snp in sortedSnpList:
        print >> outSnp, "%s" %("\t".join(snp))
    outSnp.close()