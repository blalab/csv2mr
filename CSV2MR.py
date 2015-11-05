import cPickle
from time import time
from Mapper import Mapper
from Preparer import Preparer
from Journaler import Journaler


if __name__ == '__main__':

    AI_agent = 'AVISPA'
    # Creating empty Journal
    jr = Journaler(AI_agent)

    '''MAPPING'''

    mp= Mapper(AI_agent)
    rmap = mp.run(xrn_step1=mp.rn_step1,
            xrn_step2=mp.rn_step2,
            xmmf_step1=mp.mmf_step1,
            xmmf_step2=mp.mmf_step2,
            xmmf_step3=mp.mmf_step3, 
            xmrf_step1=mp.mrf_step1)

    output = open('map_'+jr.taskname+'.pkl', 'wb')
    cPickle.dump(rmap, output)
    output.close()

    #It is better to decouple Map generation from Item preparation.

    p = open('map_'+jr.taskname+'.pkl', 'rb')
    pmap = cPickle.load(p)
    p.close()

    '''PREPARING'''

    pr = Preparer(AI_agent)
    openedfiles = pr.opener(mp.csv_filename)
    rows = pr.cat(openedfiles)
    itemlist = pr.populate(rows,pmap)
    validitemlist = pr.populate(itemlist,mp.fields)


    '''POSTING'''

    #itemlist is a generator. 
    for item in itemlist:

        jr.set(item,'new')
        post_200 = True   #Assuming this is returned by requests.post

        if post_200:     
            jr.set(item,'posted')


    print('FINAL COUNTS',jr.count)


    '''CLEANING'''

    jr.clean()
   
