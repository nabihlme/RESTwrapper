import unittest
import base64
from flask import Response
from app import *

testBody = '{"internalMetadata": { "_target" : "https://ezid.cdlib.org/id/ark:/88120/r8059v", "_profile" : "minid", "_status" : "reserved", "_export" : "no","_crossref" : "no"},"minidMetadata" : {"identifier" : "ark:/88120/r8059v","created" : "2015-11-10 04:44:44.387671", "checksum" : "cacc1abf711425d3c554277a5989df269cefaa906d27f1aaa72205d30224ed5f", "checksumMethod" : "sha1", "status" : "Active", "locations" : "http://bd2k.ini.usc.edu/assets/all-hands-meeting/minid_v0.1_Nov_2015.pdf","titles" : "minid A BD2K Minimal Viable Identifier Pilot v0.1"}}'

# removed some fields
badBody = '{"internalMetadata": {"_status" : "reserved", "_export" : "no","_crossref" : "no"},"minidMetadata" : {"minid.identifier" : "ark:/88120/r8059v","minid.created" : "2015-11-10 04:44:44.387671", "minid.checksum" : "cacc1abf711425d3c554277a5989df269cefaa906d27f1aaa72205d30224ed5f", "minid.checksumMethod" : "sha1", "minid.status" : "Active", "minid.locations" : "http://bd2k.ini.usc.edu/assets/all-hands-meeting/minid_v0.1_Nov_2015.pdf","minid.titles" : "minid: A BD2K Minimal Viable Identifier Pilot v0.1"}}'


headers = {'Authorization': 'Basic '+ base64.b64encode(b'apitest:apitest').decode('utf-8'), 'Content-Type':'application/json'}

class TestSubmission(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client() 
        
    def tearDown(self):
        # usefull for unlinking databases and removing temporary files
        pass

    def test_put_tempid(self):
        response = self.app.put('/minid/ark:/99999/fk4re4sdj', headers=headers, data= testBody)
     
        self.assertIsNotNone(response)
        self.assertIsInstance(response,Response)
        print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"success:", response.data)

   # def test_delete_tempid(self):
   #     response = self.app.delete('/minid/ark:/99999/fk4mytemp', headers=headers)
   
   #     self.assertIsNotNone(response)
   #     self.assertIsInstance(response,Response)
   #     self.assertEqual(response.status_code, 200)
   #     self.assertIn(b"success:", response.data)

if __name__ == "__main__":
    unittest.main()
