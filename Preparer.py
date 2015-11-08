import requests
import gzip
import bz2
import csv

class Preparer:

    def __init__(self,agent):
        self.AI_agent = agent   

    def opener(self,filename):
        if filename.endswith(".gz"):f = gzip.open(filename)
        elif filename.endswith(".bz2"): f = bz2.BZ2File(filename)
        else: f = open(filename)
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



    def validate(self,items,fields):

        for item in items:
            #item = {u'cc784d6f': '15952', u'4f9a647f': 'BROOKLYN', u'2aa59797': '', u'8e5b7eb1': '', u'1a3ffd3b': {'fr': '', 'en': 'Wythe Hotel started with the discovery of a factory on the Williamsburg waterfront. The building was constructed in 1901 and has been converted into a 70-room hotel. The Hotel has a rooftop bar, a gym, parking facility and a Screening Room. All the 70 rooms offer complimentary high speed Wi-Fi, flat screen LED HDTV, full-service locally sourced minibar and locally made furniture.\nThe subway stations for the lines L an G are nearby and is possible to reach Manhattan with a short ride on the subway.', 'it': "I Wythe Hotel nacque con la scoperta di una fabbrica sul lungofiume di Williamsburg. L'edificio risale al 1901 ed \xc3\xa8 stato convertito in un hotel da 70 camere. L'hotel ha un bar panoramico, una palestra, un parcheggio ed una sala cinema. Tutte le 70 camere dell'albergo sono dotate di accesso internet Wi-Fi gratuito, TV LED a schermo piatto, minibar rifornito interamente di prodotti locali e arredamento realizzato localmente. Le stazioni metropolitane per le linee L e G sono a breve distanza dall'albergo e Manhattan \xc3\xa8 facilmente raggiungibile con un breve viaggio in metropolitana.", 'sp': ''}, u'd88555ed': 'WYTHE HOTEL'}

            if self.required_field_exists(item,fields):
                pass
                #yield item
            else:
                item['_invalid'] = True
                item['_msg'] = 'Mandatory field missing or empty'
                #Last item didn't work. Ask for the next one and keep going
                print('Skipping this item, Mandatory field missing or empty')
                 


            ## VALIDATION 2
            if self.at_least_one_field_not_empty(item,fields):
                pass
            else:
                item['_invalid'] = True
                item['_msg'] = 'All fields are empty'
                #Last item didn't work. Ask for the next one and keep going
                print('Skipping this item, All fields are empty')
                

            yield item


    def required_field_exists(self,item,fields):

        for field in fields:

            if field['FieldRequired']: 
                #It is required
                if field['FieldId'] in item: 
                    #It exists   
                    if not strip(item[field['FieldId']]):
                        #It is not empty
                        return True
            else:
                #Not required
                return True

        else:
            print('Field '+field['FieldName']+'('+field['FieldId']+') is missing.')
            return False

    def at_least_one_field_not_empty(self,item,fields):

        print('Checking if item is empty:',item)

        for field in fields:

            if field['FieldId'] in item:

                if item[field['FieldId']] != '': 
                    if type(item[field['FieldId']]) is not dict:
                        print('At least one non empty field detected')
                        return True
  
        return False



            






