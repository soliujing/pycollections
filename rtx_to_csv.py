#!/usr/bin/python

import sys, getopt
import xml.etree.ElementTree as ET
import pandas as pd


def rtx_convert(input, output):
    #use pandas to convert
    tree = ET.parse(input)
    root = tree.getroot()
    ns = {'rtx':'http://schema.redwood.com/report/rtx.xsd'}

    #create new data frame
    df:pd.DataFrame = pd.DataFrame()

    # use XPATH for column names: "/table/metadata/columns/column/name" undernamespace 'rtx'
    for rtxHeader in root.findall("rtx:metadata/rtx:columns//rtx:name", ns):
        df[rtxHeader.text]=""

    # use XPATH for rtx values "/table/data/r/v" undernamespace 'rtx'
    for i in range(0, len(df.columns)):
        rtxRows = root.findall("rtx:data/rtx:r/rtx:v[" + str(i+1) + "]", ns)
        df.iloc[:, i]=pd.Series((rtxV.text for rtxV in rtxRows))
    
    # convert to csv
    df.to_csv(output, index=False)

def main(argv):
    cmdprompt='python3 rtx_to_csv.py -i <inputfile> -o <outputfile>'
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print(cmdprompt)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(cmdprompt)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    if inputfile!='' and outputfile !='' :
        rtx_convert(inputfile, outputfile)
    else :
        print(cmdprompt)

if __name__ == "__main__":
    main(sys.argv[1:])
