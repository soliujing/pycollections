#!/usr/bin/python
# %%

import sys, getopt, time
import xml.etree.ElementTree as ET
import pandas as pd
import concurrent.futures
import os, threading

def rtxV_to_df(root, ns, i):
# #use XPATH for rtx values "/table/data/r/v" undernamespace 'rtx'
    # start_time = time.time()
    # # time.sleep(1)
    # print("%02d start------>"%(i))
    # print("process : %s    , ---- thread : %s  .." % (os.getpid(), threading.currentThread().ident))
    rtxRows = root.findall("rtx:data/rtx:r/rtx:v[" + str(i+1) + "]", ns)
    # df.iloc[:, i]=pd.Series((rtxV.text for rtxV in rtxRows))
    # print("%02d end  <------ with %s seconds.. " % (i, (time.time() - start_time)))
    return rtxRows


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

# ### use threadpool executor
# ### use XPATH for rtx values "/table/data/r/v" undernamespace 'rtx'
#     p = concurrent.futures.ThreadPoolExecutor(max_workers=4)
#     futures = {}
#     for i in range(0, len(df.columns)):
#         #print("%02d new thread------>"%(i))
#         futures[i] = p.submit(rtxV_to_df, root, ns, i)
#     p.shutdown()
#     for i in range(0, len(df.columns)):
#         rtxRows = futures[i].result()
#         df.iloc[:, i]=pd.Series((rtxV.text for rtxV in rtxRows))

# # #use processpool executor
# # #use XPATH for rtx values "/table/data/r/v" undernamespace 'rtx'
#     p = concurrent.futures.ProcessPoolExecutor(max_workers=4)
#     futures = {}
#     for i in range(0, len(df.columns)):
#         #print("%02d new process------>"%(i))
#         futures[i] = p.submit(rtxV_to_df, root, ns, i)
#     p.shutdown()    
#     for i in range(0, len(df.columns)):
#         rtxRows = futures[i].result()
#         df.iloc[:, i]=pd.Series((rtxV.text for rtxV in rtxRows))


# #single thread
    for i in range(0, len(df.columns)):
        rtxRows = rtxV_to_df(root, ns, i)
        df.iloc[:, i]=pd.Series((rtxV.text for rtxV in rtxRows))
        # rtxRows = root.findall("rtx:data/rtx:r/rtx:v[" + str(i+1) + "]", ns)
        # df.iloc[:, i]=pd.Series((rtxV.text for rtxV in rtxRows))

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
    print("--- program ran about --- %s seconds ---" % (time.time() - start_time))


# %%
