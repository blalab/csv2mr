import requests
import gzip
import bz2
import csv

class Preparer:

    def __init__(self,agent):
        self.AI_agent = agent

    def opener(self,filenames):
        for name in filenames:
            if name.endswith(".gz"):f = gzip.open(name)
            elif name.endswith(".bz2"): f = bz2.BZ2File(name)
            else: f = open(name)
            yield f

    def cat(self,filelist):
        for f in filelist:
            r = csv.reader(f,delimiter=',', quotechar='"')
            for row in r:
                yield row

    def populate(self,rows,rmap):  
        for row in rows:
            item = {}
            for k in rmap:
                try:
                    if type(rmap[k]) is dict:
                        item[k] = {}
                        for lang in rmap[k]:                        
                            item[k][lang] = row[int(rmap[k][lang])-1] 
                    else:
                        item[k] = row[int(rmap[k])-1]
                except(IndexError):               
                        print("Item Corrupt, incomplete column:%s"%rmap[k] )
                        raise      
            yield item
