import os, codecs, unittest, argparse
from app import *

# figure out later
#parser = argparse.ArgumentParser(description="Give me the Username and Password So I can Test")
#parser.add_argument('Auth', metavar = 'auth', type=str, help='Username:Password for mds.test.datacite.org')
#args = parser.parse_args() 

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_getDataCenters(self):
        response = self.app.get('/data-centers')
        self.assertEqual(response.status, '200 OK')


    # List of Tests
        # post metadata
        # read in example test metadata
        #metadata = codecs.open('example.xml', 'r', encoding='utf-8').read() 
        # post doi
        # get doi
        # get metadata
        # post media
        # get media
        # delete metadata

    #def test_main(self):
    #    response = self.app.get('/doi')
    #    self.assertEqual(response.status, 401)

if __name__ == '__main__':
    unittest.main()
