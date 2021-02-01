#!/usr/bin/python
# %%

import copyreg
import io
import itertools
import sys, getopt, time
import xml.etree.ElementTree as ET
# from lxml import etree as ET
import pandas as pd
import concurrent.futures
import os, threading
from pathos.multiprocessing import ProcessingPool

ns = {'rtx':'http://schema.redwood.com/report/rtx.xsd'}

def element_tree_unpickler(data):
    # start_time = time.time()
    # a = ET.parse(io.BytesIO(data))
    # print("--- element_tree_unpickler ran about --- %3.6f seconds ---" % (time.time() - start_time))
    # return a
    return ET.parse(io.BytesIO(data))

def element_tree_pickler(element):
    # start_time = time.time()
    # a = element_tree_unpickler, (ET.tostring(element),)
    # print("--- element_tree_pickler ran about --- %3.6f seconds ---" % (time.time() - start_time))
    # return a
    return element_tree_unpickler, (ET.tostring(element),)


copyreg.pickle(ET.Element, element_tree_pickler, element_tree_unpickler)

def rtxV_to_df(root, i):
# #use XPATH for rtx values "/table/data/r/v" undernamespace 'rtx'
    # # # time.sleep(1)
    # start_time = time.time()
    # print("%02d start------>"%(i))
    # # print("process : %s    , ---- thread : %s  .." % (os.getpid(), threading.currentThread().ident))
    # print(root)

    rtxRows = root.findall("rtx:data/rtx:r/rtx:v[" + str(i+1) + "]", ns)
    rtxValues = pd.Series((rtxV.text for rtxV in rtxRows))
    # print("column %02d completed !" % (i))
    # df.iloc[:, i]=pd.Series((rtxV.text for rtxV in rtxRows))
    # print("%02d end  <------ with %3.6f seconds.. " % (i, (time.time() - start_time)))
    # return (i, rtxRows)
    return (i, rtxValues)



def rtx_convert(input, output):
    #use pandas to convert
    tree = ET.parse(input)
    root = tree.getroot()

    #create new data frame
    df:pd.DataFrame = pd.DataFrame()

    # use XPATH for column names: "/table/metadata/columns/column/name" undernamespace 'rtx'
    for rtxHeader in root.findall("rtx:metadata/rtx:columns//rtx:name", ns):
        df[rtxHeader.text]=""

    columns = len(df.columns)

### use threadpool executor
### use XPATH for rtx values "/table/data/r/v" undernamespace 'rtx'
    p = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    futures = {}
    for i in range(0, columns):
        #print("%02d new thread------>"%(i))
        futures[i] = p.submit(rtxV_to_df, root, i)
    p.shutdown()
    for i in range(0, columns):
        column, rtxRows = futures[i].result()
        df.iloc[:, column]=rtxRows

# ### user ProcessingPool and pickler & unpickler
#     res = ProcessingPool(4).map(rtxV_to_df, itertools.repeat(root,columns), range(0, columns))
#     for column, rtxRows in res:
#         # print(column)
#         # print(type(rtxRows))
#         df.iloc[:, column]=rtxRows


# # #single thread
#     for i in range(0, columns):
#         column, rtxRows = rtxV_to_df(root, i)
#         df.iloc[:, column]=rtxRows
#         # rtxRows = root.findall("rtx:data/rtx:r/rtx:v[" + str(i+1) + "]", ns)
#         # df.iloc[:, i]=pd.Series((rtxV.text for rtxV in rtxRows))

    # convert to csv
    df.to_csv(output, index=False)
    # print("done!")

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
    start_time = time.time()
    main(sys.argv[1:])
    print("--- program ran about --- %3.6f seconds ---" % (time.time() - start_time))


# %%
