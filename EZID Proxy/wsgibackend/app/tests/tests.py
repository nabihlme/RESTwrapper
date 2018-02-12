import unittest
import base64
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import *

headers = {'Authorization': 'Basic '+ base64.b64encode(b'apitest:apitest').decode('utf-8'), 'Content-Type':'application/json'}

class TestSubmission(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = True
        self.app = app.test_client() 
        
    def tearDown(self):
        # usefull for unlinking databases and removing temporary files
        pass

    def test_put_tempid(self):
        response = self.app.put('/minid/mint/ark:/99999/fk4re4sdj', headers=headers, data= testBody)
     
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
