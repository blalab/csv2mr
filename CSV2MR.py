import csv
import requests

class CSV2MR:
    

    def __init__(self):
        self.AI_agent = 'AVISPA'

    def run(self):

        print('[%s]: So, you want to import data from a CSV file to a Ring right?  '%self.AI_agent)

        csv_file = raw_input('[%s]: What is the name of the CSV file you want to import? \n[YOU]: '%self.AI_agent)
        columns = self.get_csv_header(csv_file)

        # https://avispa.myring.io/_api/teamamerica/vendortranslations

        ring_url = raw_input('[%s]: What is the URL of the Ring? \n[YOU]: '%self.AI_agent)
        ring_url_parts = ring_url.split('?')
        ring,fields = self.get_ring_schema(ring_url_parts[0]+'?schema=1')

        print('[%s]: Given the following CSV Columns:'%self.AI_agent)

        i = 0
        out = ''
        for c in columns:
            i += 1
            out += ' %s)%s'%(i,c)

        print(out)

        csv2mr_map = {}

        for f in fields:

            if f['FieldMultilingual']:
                print('[%s]: "%s" is a Multilingual field '%(self.AI_agent,f['FieldLabel']))
                langs = ['en','sp','it','fr']
                lang_dict = {}
                next_lang = True
                while next_lang:
                    r = raw_input('[%s]: Do you want to enter a new language?[yes/no] \n[YOU]: '%self.AI_agent)
                    if str(r[0]).lower() == 'y': 
                        l = raw_input('[%s]: What language you want to map?[en/sp/it/fr] \n[YOU]: '%self.AI_agent)
                        if l in langs:
                            c = raw_input('[%s]: What CSV column matches with Ring field "%s.%s"  \n[YOU]: '%(self.AI_agent,f['FieldLabel'],l))
                            lang_dict[l] = c
                        else:
                            print("[%s]: I don't recognize that language"%self.AI_agent)
                    elif str(r[0]).lower() == 'n':
                        next_lang = False


                csv2mr_map[f['FieldId']] = lang_dict


            else:
                csv2mr_map[f['FieldId']] = raw_input('[%s]: What CSV column matches with Ring field "%s" ?[1-%s] \n[YOU]: '%(self.AI_agent,f['FieldLabel'],i))

        print('[%s]: This is your map:'%self.AI_agent)
        print(csv2mr_map)


        
    def get_csv_header(self,csv_file):

        try:

            with open(csv_file,'rb') as f:
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
            csv_file = raw_input('[%s]: What is the name of the CSV file you want to import? \n[YOU]: '%self.AI_agent)
            return self.get_csv_header(csv_file)




    def get_ring_schema(self,ring_url):

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
            ring_url = raw_input('[%s]: What is the URL of the Ring? \n[YOU]: '%self.AI_agent)
            return self.get_ring_schema(ring_url)

        except(requests.exceptions.MissingSchema):

            print('[%s]: That is not a valid URL. Do you want to try another URL?'%self.AI_agent)
            ring_url = raw_input('[%s]: What is the URL of the Ring? \n[YOU]: '%self.AI_agent)
            return self.get_ring_schema(ring_url)


if __name__ == '__main__':

    c2r = CSV2MR()
    c2r.run()

    
