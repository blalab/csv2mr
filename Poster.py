import requests
import json

class Poster:

    def __init__(self,agent,target):
        self.AI_agent = agent 
        self.target = target
        print('TARGET:',self.target)

    def post(self,item):

        '''
        {u'cc784d6f': '1', Vendor
        u'4f9a647f': '2', City
        u'2aa59797': '11', Comment
        u'8e5b7eb1': '4', OriginalDescription
        u'1a3ffd3b': {'fr': '9', 'en': '8', 'it': '5', 'sp': '6'}, Translation
        u'd88555ed': '3'}  VendorName
        '''

        '''
        {u'cc784d6f': '12345',
         u'4f9a647f': 'BROOKLYN',
         u'2aa59797': 'Ready to publish', 
         u'8e5b7eb1': 'Hotel description ipsum lorem', 
         u'1a3ffd3b': {'sp': 'El otel','it':'I Hotel'}, 
         u'd88555ed': 'WYTHE HOTEL 4'}
        '''

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



