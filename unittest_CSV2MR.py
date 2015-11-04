#unitest_CSV2MR.py

import unittest
from CSV2MR import Mapper,Preparer

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
        return 'en'

    def mmf_step3(self,f,l,columns,AI_agent):
        return '1'

    def test_map_multilingual_field(self):

        self.cm.map_multilingual_field(self.f,self.columns,xmmf_step1=self.mmf_step1,xmmf_step2=self.mmf_step2,xmmf_step3=self.mmf_step3)
        self.assertEquals(self.cm.csv2mr_map['1234qwerty'],{'en':'1'})

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
        self.assertEquals(result,{u'cc784d6f': '1', u'4f9a647f': '1', u'2aa59797': '1', u'8e5b7eb1': '1', u'1a3ffd3b': {'en': '1'}, u'd88555ed': '1'})
    

class TestPreparer(unittest.TestCase):

    def setUp(self):
        self.pr = Preparer('ZOMBIE_TESTER')
        self.csv_filename = 'fixtures/TT1.csv'
        self.rows = [['936', 'YUMA', 'QUALITY INN & SUITES YUMA', 'The Comfort Inn hotel is conveniently located off Interstate 8 and U.S. Route 95, minutes from downtown Yuma, the Yuma International Airport, Old Town Yuma and the Marine Corps Air Station Yuma. This Yuma, AZ hotel is also close to the Yuma Palms Regional Center, the Yuma Proving Ground and Paradise Casino....', '', '', '', '', '', '', '', ''],
        ['15952', 'BROOKLYN', 'WYTHE HOTEL', '', "I Wythe Hotel nacque con la scoperta di una fabbrica sul lungofiume di Williamsburg. L'edificio risale al 1901 ed \xc3\xa8 stato convertito in un hotel da 70 camere. L'hotel ha un bar panoramico, una palestra, un parcheggio ed una sala cinema. Tutte le 70 camere dell'albergo sono dotate di accesso internet Wi-Fi gratuito, TV LED a schermo piatto, minibar rifornito interamente di prodotti locali e arredamento realizzato localmente. Le stazioni metropolitane per le linee L e G sono a breve distanza dall'albergo e Manhattan \xc3\xa8 facilmente raggiungibile con un breve viaggio in metropolitana.", '', '', 'Wythe Hotel started with the discovery of a factory on the Williamsburg waterfront. The building was constructed in 1901 and has been converted into a 70-room hotel. The Hotel has a rooftop bar, a gym, parking facility and a Screening Room. All the 70 rooms offer complimentary high speed Wi-Fi, flat screen LED HDTV, full-service locally sourced minibar and locally made furniture.\nThe subway stations for the lines L an G are nearby and is possible to reach Manhattan with a short ride on the subway.', '', '', '', '']]
        self.rmap = {u'cc784d6f': '1', u'4f9a647f': '2', u'2aa59797': '11', u'8e5b7eb1': '4', u'1a3ffd3b': {'fr': '9', 'en': '8', 'it': '5', 'sp': '6'}, u'd88555ed': '3'}
    

    def test_opener(self):
        l = [self.csv_filename]
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
        self.assertEquals(item['1a3ffd3b']['it'][:20],'I Wythe Hotel nacque')







if __name__ == '__main__':

    unittest.main()



