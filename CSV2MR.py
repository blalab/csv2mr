import cPickle
import json
import urlparse
import requests
from time import time
from Mapper import Mapper
from Preparer import Preparer
from Journaler import Journaler
from Poster import Poster

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

    output = open(jr.journal_root+'map_'+jr.taskname+'.pkl', 'wb')
    cPickle.dump(rmap, output)
    output.close()

    #It is better to decouple Map generation from Item preparation.

    p = open(jr.journal_root+'map_'+jr.taskname+'.pkl', 'rb')
    pmap = cPickle.load(p)
    p.close()

    '''PREPARING'''

    pr = Preparer(AI_agent)
    openedfiles = pr.opener(mp.csv_filename)
    rows = pr.cat(openedfiles)
    itemlist = pr.populate(rows,pmap)
    validitemlist = pr.validate(itemlist,mp.fields)


    '''POSTING'''

    #itemlist is a generator. 
    pr = Poster(AI_agent,mp.ring_url)

    for item in validitemlist:

        if '_invalid' in item:
            jr.set(item,'invalid')
        else:
            if not jr.set(item,'new'): # Record your intent in the journal
                continue  # if false we should not post it. 

                '''
                Validation vs Journaler errors
                Validation is able to detect errors in the item
                Journaler is able to detect errors across items
                '''

            result = pr.post(item)
            r = json.loads(result.text)
            print(r)

            # Record result in Journal
            if result.status_code == requests.codes.ok: 
                if r['Success']:
                    o = urlparse.urlparse(mp.ring_url)
                    item['_uri'] = urlparse.urlunparse((o.scheme, o.netloc, r['item'], '', '', ''))  
                    jr.set(item,'posted') # Update the journal on success
                else:
                    item['_error'] = True
                    item['_msg'] = r['Message']
                    jr.set(item,'error')
            else:
                item['_error'] = True
                item['_msg'] = 'status'+str(result.status_code)
                jr.set(item,str(result.status_code))



    print('FINAL COUNTS',jr.count)

    '''CLEANING'''

    jr.clean()
   
