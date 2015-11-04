import requests
import gzip
import bz2
import csv

def opener(filenames):
    for name in filenames:
        if name.endswith(".gz"):f = gzip.open(name)
        elif name.endswith(".bz2"): f = bz2.BZ2File(name)
        else: f = open(name)
        yield f

def cat(filelist):
    for f in filelist:
        r = csv.reader(f,delimiter=',', quotechar='"')
        for row in r:
            yield row

def populate(rows,rmap):  
    for row in rows:
        #l = line.split(',')
        print('Try:',row)
        #print(rmap)
        item = {}
        for k in rmap:
            #print(k)
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
            
                

'''
sample = 1097,YUMA,SHILO INN YUMA,"Gracious Southwestern furnishings and a friendly staff set the stage for a memorable visit at the Shilo Inn Yuma. This full-service hotel features 135 guestrooms with microwaves, refrigerators, coffee makers, data ports and ironing units. After a long day of meetings, shopping or sight seeing,luxuriate in our spa or Olympic-sized pool. High speed Internet access now available in all rooms.",,,,,,,,
'''

rmap = {u'cc784d6f': '1', u'4f9a647f': '2', u'2aa59797': '11', u'8e5b7eb1': '4', u'1a3ffd3b': {'fr': '9', 'en': '8', 'it': '5', 'sp': '6'}, u'd88555ed': '3'}

filelist = ['TT1.csv']
openedfiles = opener(filelist)
lines = cat(openedfiles)
itemlist = populate(lines,rmap)

count = 0

for item in itemlist:
    count += 1
    print(item)

print('Total Items:%s'%count)
