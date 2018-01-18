import os
import unittest
from app import *

class FlaskTestCase(unittest.TestCase):

    # set up and tear down
    def setUp(self):
        app.config['Testing'] = True
        app.config['Debug'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    # List of Tests
    def test_main(self):
        response = self.app.get('/doi')
        self.assertEqual(response.status, 401)

if __name__ == '__main__':
    unittest.main()
