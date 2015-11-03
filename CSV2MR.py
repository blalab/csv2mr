from Mapper import Mapper
from Preparer import Preparer


if __name__ == '__main__':

    mp= Mapper()
    rmap = mp.run(xrn_step1=mp.rn_step1,
            xrn_step2=mp.rn_step2,
            xmmf_step1=mp.mmf_step1,
            xmmf_step2=mp.mmf_step2,
            xmmf_step3=mp.mmf_step3, 
            xmrf_step1=mp.mrf_step1)

    pr = Preparer()
    filelist = ['TT1.csv']
    openedfiles = pr.opener(filelist)
    rows = pr.cat(openedfiles)
    itemlist = pr.populate(rows,rmap)

    count = 0

    #itemlist is a generator. 

    for item in itemlist:
        count += 1
        print(item)

    print('Total Items:%s'%count)
   
