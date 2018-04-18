#!/usr/bin/env python

import os
import sys

#Parse a config file to be usable
def parseFile (fileLoc):
    #open the file
    try:
        f = open(fileLoc)
        #get rid of comments, and make this file usable	
        sshOptList = []
        sshOptList = [{'config_file': fileLoc}]
        for line in f:
            line = line.split()
            if line and "#" not in line[0]:
                key = line[0]
                val = " ".join(str(x) for x in line[1:])
                newDict = {
                    key:val
                }   
                sshOptList.append(newDict)
        f.close()    
        return sshOptList
    
#if the file doesn't exist, die
    except IOError:
        print "File %s Not Found" % fileLoc
        exit()
