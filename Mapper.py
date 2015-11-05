import csv
import requests

class Mapper:
    

    def __init__(self,agent):
        self.AI_agent = agent
        self.csv2mr_map = {}

    @staticmethod
    def rn_step1(AI_agent):

        return raw_input('[%s]: What is the name of the CSV file you want to import? \n[YOU]: '%AI_agent)
  
    def rn_step2(self,AI_agent):

        return raw_input('[%s]: What is the URL of the Ring? \n[YOU]: '%AI_agent)
  
    def mmf_step1(self,AI_agent):

        return raw_input('[%s]: Do you want to enter a new language?[yes/no] \n[YOU]: '%AI_agent)

    
    def mmf_step2(self,langs,AI_agent):

        return raw_input('[%s]: What language you want to map?[%s] \n[YOU]: '%(AI_agent,'/'.join(langs)))

    
    def mmf_step3(self,f,l,columns,AI_agent):

        return raw_input('[%s]: What CSV column matches with Ring field "%s.%s" ?[1-%s]  \n[YOU]: '%(
                                   AI_agent,
                                   f['FieldLabel'],
                                   l,
                                   len(columns)))

    def mrf_step1(self,f,columns,AI_agent):

        return raw_input('[%s]: What CSV column matches with ring field "%s" ?[1-%s] \n[YOU]: '% (
                                                           AI_agent,
                                                           f['FieldLabel'],
                                                           len(columns)))

    def run(self,
            xrn_step1=rn_step1,
            xrn_step2=rn_step2,
            xmmf_step1=mmf_step1,
            xmmf_step2=mmf_step2,
            xmmf_step3=mmf_step3, 
            xmrf_step1=mrf_step1):

        print('[%s]: So, you want to import data from a CSV file to a Ring right?  '%self.AI_agent)

        self.csv_filename = xrn_step1(self.AI_agent)
        columns = self.get_csv_header(self.csv_filename)

        self.ring_url = xrn_step2(self.AI_agent)
        ring_url_parts = self.ring_url.split('?')
        self.ring,self.fields = self.get_ring_schema(ring_url_parts[0]+'?schema=1')

        print('[%s]: Given the following CSV Columns:'%self.AI_agent)
        print(self.columns_menu_string(columns))

        
        for f in self.fields:
            if f['FieldMultilingual']:
                self.map_multilingual_field(f,
                                            columns,
                                            xmmf_step1=xmmf_step1,
                                            xmmf_step2=xmmf_step2,
                                            xmmf_step3=xmmf_step3)
            else:
                self.map_regular_field(f,columns,xmrf_step1=xmrf_step1)

        print('[%s]: This is your map:'%self.AI_agent)
        print(self.csv2mr_map)
        return self.csv2mr_map


    def map_regular_field(self,f,columns,xmrf_step1=mrf_step1):

        self.csv2mr_map[f['FieldId']] = xmrf_step1(f,columns,self.AI_agent)


    def map_multilingual_field(self,f,columns,xmmf_step1=None,xmmf_step2=None,xmmf_step3=None):

        print('[%s]: "%s" is a Multilingual field '%(self.AI_agent,f['FieldLabel']))
        langs = ['en','sp','it','fr']
        lang_dict = {}
        next_lang = True
        while next_lang:
            r = xmmf_step1(self.AI_agent)
            if str(r[0]).lower() == 'y': 
                l = xmmf_step2(langs,self.AI_agent)
                if l in langs:
                    c = xmmf_step3(f,l,columns,self.AI_agent)
                    lang_dict[l] = c
                else:
                    print("[%s]: I don't recognize that language"%self.AI_agent)
            elif str(r[0]).lower() == 'n':
                next_lang = False


        self.csv2mr_map[f['FieldId']] = lang_dict

    def columns_menu_string(self,columns):

        i = 0
        out = ''
        for c in columns:
            i += 1
            out += ' %s)%s'%(i,c)

        return out


    def retry_get_csv_header(self,raw_input):

        csv_filename = raw_input('[%s]: What is the name of the CSV file you want to import? \n[YOU]: '%self.AI_agent)
        return self.get_csv_header(csv_filename)

        
    def get_csv_header(self,csv_filename,retry_raw_input=raw_input):

        try:

            with open(csv_filename,'rb') as f:
                self.reader = csv.reader(f)

                for row in self.reader:
                    #print(row)
                    csv_header=[]
                    count = 0

                    for r in row:
                        #print(type(r))

                        if r != '':
                            csv_header.append(r)
                            count += 1
                    
                    if count != 0:
                        break

                print('[%s]: %s columns detected: '%(self.AI_agent,len(csv_header)))
                print(', '.join(csv_header))

                return csv_header

        except(IOError):

            print('[%s]: There was a problem opening that file. '%self.AI_agent)
            print('[%s]: It should live in the same folder as this script. '%self.AI_agent)
            return self.retry_get_csv_header(retry_raw_input)

    def retry_get_ring_schema(self,raw_input):
        
        ring_url = raw_input('[%s]: What is the URL of the Ring? \n[YOU]: '%self.AI_agent)
        return self.get_ring_schema(ring_url)


    def get_ring_schema(self,ring_url,retry_raw_input=raw_input):

        try:

            r = requests.get(ring_url)

            if r.status_code == requests.codes.ok:

                #print(r.json())
                fields = r.json()['fields']
                rings = r.json()['rings']

                print('[%s]: Got it!'%self.AI_agent)
                print('[%s]: %s fields detected: '%(self.AI_agent,len(fields)))   
                print(', '.join([field['FieldLabel'] for field in fields]))

                return rings,fields

            else:
                raise

        except(ValueError):
            print('[%s]: There was a problem with that URL. Do you want to try another URL?'%self.AI_agent)
            return self.retry_get_ring_schema(retry_raw_input)

        except(requests.exceptions.MissingSchema):
            print('[%s]: That is not a valid URL. Do you want to try another URL?'%self.AI_agent)
            return self.retry_get_ring_schema(retry_raw_input)

        except(requests.exceptions.ConnectionError):
            print('[%s]: Connection refused. Do you want to try another URL?'%self.AI_agent)
            return self.retry_get_ring_schema(retry_raw_input)