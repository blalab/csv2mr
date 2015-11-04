import cPickle
from time import time
from Mapper import Mapper
from Preparer import Preparer


if __name__ == '__main__':

    AI_agent = 'AVISPA'

    taskname = str(int(time()))

    '''MAPPING'''

    mp= Mapper(AI_agent)
    rmap = mp.run(xrn_step1=mp.rn_step1,
            xrn_step2=mp.rn_step2,
            xmmf_step1=mp.mmf_step1,
            xmmf_step2=mp.mmf_step2,
            xmmf_step3=mp.mmf_step3, 
            xmrf_step1=mp.mrf_step1)

    output = open('map_'+taskname+'.pkl', 'wb')
    cPickle.dump(rmap, output)
    output.close()

    #It is better to decouple Map generation from Item preparation.

    '''PREPARING'''
    p = open('map_'+taskname+'.pkl', 'rb')
    pmap = cPickle.load(p)
    p.close()

    pr = Preparer(AI_agent)
    filelist = ['TT1.csv']
    openedfiles = pr.opener(filelist)
    rows = pr.cat(openedfiles)
    itemlist = pr.populate(rows,pmap)


    '''POSTING'''

    # Creating empty Journal
    jrn = Journaler(AI_agent,taskname)

    #itemlist is a generator. 
    for item in itemlist:
        post_200 = True   #Assuming this is returned by requests.post

        if post_200:     
            jrn.insert(item)

    jrn.close()


    print('Total OK Items:%s'%jrn.count_ok)
    print('Total Errors:%s'%jrn.count_error)
   
