#unitest_CSV2MR.py

import unittest
from CSV2MR import CSV2MR

class TestFunctionality(unittest.TestCase):

    def setUp(self):

        self.cm = CSV2MR()
        self.csv_filename = 'TT1.csv'
        self.incorrect_csv_filename = 'TTxxx.csv'
        self.ring_url = 'https://avispa.myring.io/_api/teamamerica/vendortranslations?schema=1'
        self.incorrect_ring_url = 'https://avispax.myring.io/_api/teamamerica/vendortranslations?schema=1'
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
    


if __name__ == '__main__':

    unittest.main()



