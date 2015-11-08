import requests
import json

class Poster:

    def __init__(self,agent,target):
        self.AI_agent = agent 
        self.target = target
        print('TARGET:',self.target)

    def post(self,item):


        #Convert objects into JSON
        print(item)
        for k,v in item.iteritems():
            if type(v) is dict:
                item[k] = json.dumps(v) 

        
        print('POST',self.target,item)

        r = requests.post(self.target,data=item)


        print(r.status_code)
        print(r.headers)
        print('TEXT:',r.text)

        return r



