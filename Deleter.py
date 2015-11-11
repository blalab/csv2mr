import json
import requests
import urlparse
from Journaler import Journaler

class Deleter:
    

    def __init__(self,agent,journal_root):
        self.AI_agent = agent 
        self.journal_root = journal_root
        

    def delete(self,uri):

        # Detect and repair if not API ready
        o = urlparse.urlparse(uri)
        parts = o.path.split('/')
        if parts[1] != '_api':
            path = '_api'+o.path
        else:
            path = o.path

        uri = urlparse.urlunparse((o.scheme,o.netloc,path,'','',''))

        payload = {'method':'delete'}
        #r = requests.delete(uri,data=payload)
        print('Delete:'+uri)
        result = requests.get(uri,params=payload)

        print(result.status_code)
        print(result.headers)
        print('TEXT:',result.text)

        q = json.loads(result.text)
        #{"uri": "teamamerica/vendortranslations/7997386758", "success": true, "method": "DELETE"}
        if q['success'] and q['uri']==o.path and result.status_code == requests.codes.ok:
            return True
        else:
            return False
        

    def unpost(self,taskname=None):

        if not taskname:
            taskname = raw_input('[%s]: What task you want to unpost? \n[YOU]: '%self.AI_agent)

        with open(self.journal_root+'posted_items_'+taskname+'.txt', 'rb+') as f:
            for line in f:               
                l = json.loads(line)
                print('Attempting to delete:'+str(l['uri']))
 
                o = urlparse.urlparse(str(l['uri']))
                url_api = urlparse.urlunparse((o.scheme,o.netloc,'_api'+o.path,'','',''))
                if self.delete(url_api):
                    f.write("%s %s\n" % ('DELETED',line))
                else:
                    f.write("%s %s\n" % ('NOT DELETED',line))
           


if __name__ == '__main__':

    dl = Deleter('AVISPA','Journal/')
    dl.unpost()



