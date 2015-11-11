#unitest_CSV2MR.py

import unittest
import time
import json
import os
import urlparse
from Mapper import Mapper
from Preparer import Preparer
from Journaler import Journaler
from Poster import Poster
from Deleter import Deleter

class TestMapper(unittest.TestCase):

    def setUp(self):

        self.cm = Mapper('ZOMBIE_TESTER')
        self.csv_filename = 'fixtures/TT1.csv'
        self.incorrect_csv_filename = 'fixtures/TTxxx.csv'
        #TO DO: mock this call
        self.ring_url = 'https://avispa.myring.io/_api/teamamerica/vendortranslations?schema=1'
        self.incorrect_ring_url = 'https://avispax.myring.io/_api/xxx/yyy?schema=1'
        self.invalid_ring_url = 'invalidurl'
        self.columns = ['Option_1','Option_2']
        self.f = {'FieldLabel':'Name','FieldId':'1234qwerty'}
        self.count_1 = 0

    def correct_csv_filename_raw_input(self,prompt):
        return self.csv_filename

    def correct_ring_url_raw_input(self,prompt):
        return self.ring_url
    

    def test_get_csv_header(self):

        result = self.cm.get_csv_header(self.csv_filename)
        self.assertEquals(result[1],'City')

    def test_get_incorrect_csv_header(self):

        result = self.cm.get_csv_header(self.incorrect_csv_filename,retry_raw_input=self.correct_csv_filename_raw_input)
        self.assertEquals(result[1],'City')

    def test_get_ring_schema(self):

        rings,fields = self.cm.get_ring_schema(self.ring_url)
        self.assertEquals(fields[0]['FieldName'],'vendorid')
    
    def test_get_ring_schema_with_incorrect_url(self):

        rings,fields = self.cm.get_ring_schema(self.incorrect_ring_url,retry_raw_input=self.correct_ring_url_raw_input)
        self.assertEquals(fields[0]['FieldName'],'vendorid')

    
    def test_get_ring_schema_with_invalid_url(self):

        rings,fields = self.cm.get_ring_schema(self.invalid_ring_url,retry_raw_input=self.correct_ring_url_raw_input)
        self.assertEquals(fields[0]['FieldName'],'vendorid')

    def test_columns_menu_string(self):

        result = self.cm.columns_menu_string(self.columns)
        self.assertEquals(' 1)Option_1 2)Option_2',result)

    def rn_step1(self,AI_agent):

        return self.csv_filename

    def rn_step2(self,AI_agent):

        return self.ring_url

    def mmf_step1(self,AI_agent):

        tries = 1

        if self.count_1 < tries:
            self.count_1 += 1
            return 'yes'
        else:
            return 'no'

    def mmf_step2(self,langs,AI_agent):
        return 'eng'

    def mmf_step3(self,f,l,columns,AI_agent):
        return '1'

    def test_map_multilingual_field(self):

        self.cm.map_multilingual_field(self.f,self.columns,xmmf_step1=self.mmf_step1,xmmf_step2=self.mmf_step2,xmmf_step3=self.mmf_step3)
        self.assertEquals(self.cm.csv2mr_map['1234qwerty'],{'eng':'1'})

    def mrf_step1(self,f,columns,AI_agent):
        return '1'

    '''
    def test_map_regular_field(self):

        self.cm.map_regular_field(self.f,self.columns,mrf_step1=self.mrf_step1)
        self.assertEquals(self.cm.csv2mr_map['1234qwerty'],'1')
    '''

    
    def test_run(self):

        result = self.cm.run(
            xrn_step1=self.rn_step1,
            xrn_step2=self.rn_step2,
            xmmf_step1=self.mmf_step1,
            xmmf_step2=self.mmf_step2,
            xmmf_step3=self.mmf_step3, 
            xmrf_step1=self.mrf_step1)
        self.assertEquals(result,{u'cc784d6f': '1', u'4f9a647f': '1', u'2aa59797': '1', u'8e5b7eb1': '1', u'1a3ffd3b': {'eng': '1'}, u'd88555ed': '1'})
    

class TestPreparer(unittest.TestCase):

    def setUp(self):
        self.pr = Preparer('ZOMBIE_TESTER')
        self.csv_filename = 'fixtures/TT1.csv'
        self.rows = [['936', 'YUMA', 'QUALITY INN & SUITES YUMA', 'The Comfort Inn hotel is conveniently located off Interstate 8 and U.S. Route 95, minutes from downtown Yuma, the Yuma International Airport, Old Town Yuma and the Marine Corps Air Station Yuma. This Yuma, AZ hotel is also close to the Yuma Palms Regional Center, the Yuma Proving Ground and Paradise Casino....', '', '', '', '', '', '', '', ''],
        ['15952', 'BROOKLYN', 'WYTHE HOTEL', '', "I Wythe Hotel nacque con la scoperta di una fabbrica sul lungofiume di Williamsburg. L'edificio risale al 1901 ed \xc3\xa8 stato convertito in un hotel da 70 camere. L'hotel ha un bar panoramico, una palestra, un parcheggio ed una sala cinema. Tutte le 70 camere dell'albergo sono dotate di accesso internet Wi-Fi gratuito, TV LED a schermo piatto, minibar rifornito interamente di prodotti locali e arredamento realizzato localmente. Le stazioni metropolitane per le linee L e G sono a breve distanza dall'albergo e Manhattan \xc3\xa8 facilmente raggiungibile con un breve viaggio in metropolitana.", '', '', 'Wythe Hotel started with the discovery of a factory on the Williamsburg waterfront. The building was constructed in 1901 and has been converted into a 70-room hotel. The Hotel has a rooftop bar, a gym, parking facility and a Screening Room. All the 70 rooms offer complimentary high speed Wi-Fi, flat screen LED HDTV, full-service locally sourced minibar and locally made furniture.\nThe subway stations for the lines L an G are nearby and is possible to reach Manhattan with a short ride on the subway.', '', '', '', '']]
        self.rmap = {u'cc784d6f': '1', u'4f9a647f': '2', u'2aa59797': '11', u'8e5b7eb1': '4', u'1a3ffd3b': {'fra': '9', 'eng': '8', 'ita': '5', 'spa': '6'}, u'd88555ed': '3'}
        self.firstrowsempty = [['', '', '', '', '', '', '', '', '', '', '', ''],
        ['15952', 'BROOKLYN', 'WYTHE HOTEL', '', "I Wythe Hotel nacque con la scoperta di una fabbrica sul lungofiume di Williamsburg. L'edificio risale al 1901 ed \xc3\xa8 stato convertito in un hotel da 70 camere. L'hotel ha un bar panoramico, una palestra, un parcheggio ed una sala cinema. Tutte le 70 camere dell'albergo sono dotate di accesso internet Wi-Fi gratuito, TV LED a schermo piatto, minibar rifornito interamente di prodotti locali e arredamento realizzato localmente. Le stazioni metropolitane per le linee L e G sono a breve distanza dall'albergo e Manhattan \xc3\xa8 facilmente raggiungibile con un breve viaggio in metropolitana.", '', '', 'Wythe Hotel started with the discovery of a factory on the Williamsburg waterfront. The building was constructed in 1901 and has been converted into a 70-room hotel. The Hotel has a rooftop bar, a gym, parking facility and a Screening Room. All the 70 rooms offer complimentary high speed Wi-Fi, flat screen LED HDTV, full-service locally sourced minibar and locally made furniture.\nThe subway stations for the lines L an G are nearby and is possible to reach Manhattan with a short ride on the subway.', '', '', '', '']]
        self.fields = [{u'FieldLabel': u'VendorID', u'FieldOrder': u'1', u'FieldDefault': u'', u'FieldSource': u'', u'FieldLayer': u'2', u'FieldRequired': False, u'FieldWidget': u'text', u'FieldHint': u'', u'FieldMultilingual': False, u'FieldName': u'vendorid', u'FieldType': u'STRING', u'FieldId': u'cc784d6f', u'FieldCardinality': u'Single', u'FieldSemantic': u''}, {u'FieldLabel': u'City', u'FieldOrder': u'2', u'FieldDefault': u'', u'FieldSource': u'', u'FieldLayer': u'2', u'FieldRequired': False, u'FieldWidget': u'text', u'FieldHint': u'', u'FieldMultilingual': False, u'FieldName': u'city', u'FieldType': u'STRING', u'FieldId': u'4f9a647f', u'FieldCardinality': u'Single', u'FieldSemantic': u''}, {u'FieldLabel': u'VendorName', u'FieldOrder': u'3', u'FieldDefault': u'', u'FieldSource': u'', u'FieldLayer': u'1', u'FieldRequired': False, u'FieldWidget': u'text', u'FieldHint': u'', u'FieldMultilingual': False, u'FieldName': u'vendorname', u'FieldType': u'STRING', u'FieldId': u'd88555ed', u'FieldCardinality': u'Single', u'FieldSemantic': u''}, {u'FieldLabel': u'OriginalDescription', u'FieldOrder': u'4', u'FieldDefault': u'', u'FieldSource': u'', u'FieldLayer': u'3', u'FieldRequired': False, u'FieldWidget': u'textarea', u'FieldHint': u'', u'FieldMultilingual': False, u'FieldName': u'originaldescription', u'FieldType': u'STRING', u'FieldId': u'8e5b7eb1', u'FieldCardinality': u'Single', u'FieldSemantic': u''}, {u'FieldLabel': u'Translation', u'FieldOrder': u'5', u'FieldDefault': u'', u'FieldSource': u'', u'FieldLayer': u'3', u'FieldRequired': False, u'FieldWidget': u'textarea_multilang', u'FieldHint': u'', u'FieldMultilingual': u'1', u'FieldName': u'translation', u'FieldType': u'OBJECT', u'FieldId': u'1a3ffd3b', u'FieldCardinality': u'Single', u'FieldSemantic': u''}, {u'FieldLabel': u'Comment', u'FieldOrder': u'6', u'FieldDefault': u'', u'FieldSource': u'', u'FieldLayer': u'3', u'FieldRequired': False, u'FieldWidget': u'textarea', u'FieldHint': u'', u'FieldMultilingual': False, u'FieldName': u'comment', u'FieldType': u'STRING', u'FieldId': u'2aa59797', u'FieldCardinality': u'Single', u'FieldSemantic': u''}]

    def test_opener(self):
        l = self.csv_filename
        openedfiles = self.pr.opener(l)
        f = openedfiles.next()  
        self.assertEquals(type(f),file)

    def test_cat(self):
        openedfileslist = [open(self.csv_filename)]
        openedfiles = (f for f in openedfileslist)
        lines = self.pr.cat(openedfiles)
        lines.next() # First line comes empty
        line = lines.next()
        self.assertEquals(line[1],'City')

    def test_populate(self):
        itemlist = self.pr.populate(self.rows,self.rmap)
        item = itemlist.next()
        self.assertEquals(item['cc784d6f'],'936')

    def test_populate_with_languages(self):
        itemlist = self.pr.populate(self.rows,self.rmap)
        itemlist.next() #Let the first item pass
        item = itemlist.next()
        self.assertEquals(item['1a3ffd3b']['ita'][:20],'I Wythe Hotel nacque')

    def test_validate(self):
        itemlist = self.pr.populate(self.rows,self.rmap)
        validitemlist = self.pr.validate(itemlist,self.fields)
        validitemlist.next()
        item = validitemlist.next()
        self.assertEquals(item['1a3ffd3b']['ita'][:20],'I Wythe Hotel nacque')

    def test_validate_detects_first_item_empty(self):
        itemlist = self.pr.populate(self.firstrowsempty,self.rmap)
        validitemlist = self.pr.validate(itemlist,self.fields)
        item = validitemlist.next()
        self.assertEquals(item['_msg'],'All fields are empty')



class TestJournaler(unittest.TestCase):

    def setUp(self):
        self.jr = Journaler('ZOMBIE TESTER')
        self.item = {u'cc784d6f': 'BROOKLYN', 
                     u'4f9a647f': 'WYTHE HOTEL', 
                     u'2aa59797': '', 
                     u'8e5b7eb1': "I Wythe Hotel nacque con la scoperta di una fabbrica sul lungofiume di Williamsburg. L'edificio risale al 1901 ed \xc3\xa8 stato convertito in un hotel da 70 camere. L'hotel ha un bar panoramico, una palestra, un parcheggio ed una sala cinema. Tutte le 70 camere dell'albergo sono dotate di accesso internet Wi-Fi gratuito, TV LED a schermo piatto, minibar rifornito interamente di prodotti locali e arredamento realizzato localmente. Le stazioni metropolitane per le linee L e G sono a breve distanza dall'albergo e Manhattan \xc3\xa8 facilmente raggiungibile con un breve viaggio in metropolitana.", 
                     u'1a3ffd3b': {'spa': ''}, 
                     u'd88555ed': ''}

        self.invalid_item = {u'invalid':True,
                     u'errormsg': 'Mandatory field missing or empty',
                     u'cc784d6f': 'BROOKLYN', 
                     u'4f9a647f': 'WYTHE HOTEL', 
                     u'2aa59797': '', 
                     u'8e5b7eb1': "I Wythe Hotel nacque con la scoperta di una fabbrica sul lungofiume di Williamsburg. L'edificio risale al 1901 ed \xc3\xa8 stato convertito in un hotel da 70 camere. L'hotel ha un bar panoramico, una palestra, un parcheggio ed una sala cinema. Tutte le 70 camere dell'albergo sono dotate di accesso internet Wi-Fi gratuito, TV LED a schermo piatto, minibar rifornito interamente di prodotti locali e arredamento realizzato localmente. Le stazioni metropolitane per le linee L e G sono a breve distanza dall'albergo e Manhattan \xc3\xa8 facilmente raggiungibile con un breve viaggio in metropolitana.", 
                     u'1a3ffd3b': {'spa': ''}, 
                     u'd88555ed': ''}

    def tearDown(self):
        self.jr.clean()

        
        if os.path.isfile(self.jr.journal_root+'posted_items_'+self.jr.taskname+'.txt'):
            os.remove(self.jr.journal_root+'posted_items_'+self.jr.taskname+'.txt')
        

        if os.path.isfile(self.jr.journal_root+'invalid_items_'+self.jr.taskname+'.txt'):
            os.remove(self.jr.journal_root+'invalid_items_'+self.jr.taskname+'.txt')

        if os.path.isfile(self.jr.journal_root+'repeated_items_'+self.jr.taskname+'.txt'):
            os.remove(self.jr.journal_root+'repeated_items_'+self.jr.taskname+'.txt')
        

    def test_set_get_new_item(self):

        self.jr.set(self.item,'new')
        result = self.jr.get(self.item)
        self.assertEquals(result['s'],'new')

    def test_post_item(self):

        self.jr.set(self.item,'new')
        self.jr.set(self.item,'posted')
        result = self.jr.get(self.item)
        self.assertEquals(result['s'],'posted')

    def test_post_item_outfile(self):

        self.jr.set(self.item,'new')
        self.jr.set(self.item,'posted')
        result = self.jr.get(self.item)
        self.assertEquals(result['s'],'posted')

    def test_increase_count(self):

        self.jr.increase_count('x')
        self.jr.increase_count('x')
        self.jr.increase_count('x')
        self.jr.increase_count('y')
        self.jr.increase_count('y')
        self.jr.increase_count('x')

        self.assertEquals(self.jr.count['x'],4)

    def test_set_a_duplicate_item(self):

        self.jr.set(self.item,'new')
        result = self.jr.set(self.item,'new')       
        self.assertFalse(result)

    def test_set_a_duplicate_counter(self):

        self.jr.set(self.item,'new')
        self.jr.set(self.item,'new')  
        self.assertEquals(self.jr.count['repeated'],1)

    def test_set_an_invalid_item(self):

        self.jr.set(self.invalid_item,'invalid')
        result = self.jr.get(self.invalid_item)
        self.assertEquals(result['s'],'invalid')


class TestPoster(unittest.TestCase):

    def setUp(self):
        self.ring_url = 'https://avispa.myring.io/_api/teamamerica/vendortranslations?schema=1'
        self.item = {u'cc784d6f': '12345',
                     u'4f9a647f': 'BROOKLYN',
                     u'2aa59797': 'Ready to publish', 
                     u'8e5b7eb1': 'Hotel description ipsum lorem', 
                     u'1a3ffd3b': {'spa': 'El otel','ita':'I Hotel'}, 
                     u'd88555ed': 'WYTHE HOTEL 5'}

        self.item1 = {u'cc784d6f': '12345',
                     u'4f9a647f': 'BROOKLYN',
                     u'2aa59797': 'Ready to publish', 
                     u'8e5b7eb1': 'Hotel description ipsum lorem', 
                     u'1a3ffd3b': {'spa': 'El otel','ita':'I Hotel'}, 
                     u'd88555ed': 'Adams Family House'}

        self.item2 = {u'cc784d6f': '12345',
                     u'4f9a647f': 'BROOKLYN',
                     u'2aa59797': 'Ready to publish', 
                     u'8e5b7eb1': 'Hotel description ipsum lorem', 
                     u'1a3ffd3b': {'spa': 'El otel','ita':'I Hotel'}, 
                     u'd88555ed': 'Castillo de Greyskull'}

        self.item3 = {u'cc784d6f': '12345',
                     u'4f9a647f': 'BROOKLYN',
                     u'2aa59797': 'Ready to publish', 
                     u'8e5b7eb1': 'Hotel description ipsum lorem', 
                     u'1a3ffd3b': {'spa': 'El otel','ita':'I Hotel'}, 
                     u'd88555ed': 'Taberna de Moe'}

        self.emptyitem = {u'cc784d6f': '',
                     u'4f9a647f': 'BROOKLYN',
                     u'2aa59797': '', 
                     u'8e5b7eb1': '', 
                     u'1a3ffd3b': {}, 
                     u'd88555ed': ''}

        
        self.pr = Poster('ZOMBIE_TESTER',self.ring_url)

        self.items_to_delete = []

    def tearDown(self):
        dl = Deleter('ZOMBIE_TESTER','Journal/')
        o = urlparse.urlparse(self.ring_url)
        
        for item in self.items_to_delete:
            url_api = urlparse.urlunparse((o.scheme,o.netloc,item,'','',''))
            dl.delete(url_api)


    @unittest.skip('')
    def test_post(self):

        result = self.pr.post(self.item)
        r = json.loads(result.text)
        print(r)
        
        self.ring_url
        self.items_to_delete.append(r['item'])
        
        #print(r.Success)
        #u"{'item': 'teamamerica/vendortranslations/8420377079', 'Message': 'Item saved', 'Success': True}"
        self.assertEquals(r['Success'],True)

    @unittest.skip('')
    def test_post_multiple(self):

        result1 = self.pr.post(self.item1)
        r1 = json.loads(result1.text)
        print(r1)
        self.items_to_delete.append(r1['item'])
        result2 = self.pr.post(self.item2)
        r2 = json.loads(result2.text)
        print(r2)
        self.items_to_delete.append(r2['item'])
        result3 = self.pr.post(self.item3)
        r3 = json.loads(result3.text)
        print(r3)
        self.items_to_delete.append(r3['item'])

        self.assertEquals(r1['Success'] and r2['Success'] and r3['Success']  ,True)

    def test_post_empty_fields_item(self):

        result = self.pr.post(self.emptyitem)
        r = json.loads(result.text)
        print(r)
        self.items_to_delete.append(r['item'])
        self.assertEquals(r['Success'],True)


class TestDeleter(unittest.TestCase):

    def setUp(self):
        pass










if __name__ == '__main__':

    unittest.main()



