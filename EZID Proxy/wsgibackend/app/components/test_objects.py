import unittest
from objects import *


#============================================================================================#
# incoming test json payload
JSON = '{"identifier": "ark:/99999/fk4r8059v","created": "2015-11-10 04:44:44.387671","creator": "0000-0003-2129-5269","checksum": "cacc1abf711425d3c554277a5989df269cefaa906d27f1aaa72205d30224ed5f","checksumMethod":"sha1","status": "ACTIVE","locations": ["http://bd2k.ini.usc.edu/assets/all-hands-meeting/minid_v0.1_Nov_2015.pdf"],"titles": ["minid: A BD2K Minimal Viable Identifier Pilot v0.1"]}'

# correctly mapped json payload
JSONdict = { "identifier": "ark:/99999/fk4r8059v", \
        "created": "2015-11-10 04:44:44.387671", \
                "creator": "0000-0003-2129-5269", \
                "checksum": "cacc1abf711425d3c554277a5989df269cefaa906d27f1aaa72205d30224ed5f", \
                "checksumMethod":"sha1", \
                "status": "ACTIVE", \
                "locations": ["http://bd2k.ini.usc.edu/assets/all-hands-meeting/minid_v0.1_Nov_2015.pdf"], \
                "titles": ["minid: A BD2K Minimal Viable Identifier Pilot v0.1"] \
                }

# incoming anvl
ANVL = b'_target: ark:/99999/fk4r8059v\n_profile: minid\n_status: reserved\nminid.created: 2015-11-10 04:44:44.387671\nminid.creator: 0000-0003-2129-5269\nminid.checksum: cacc1abf711425d3c554277a5989df269cefaa906d27f1aaa72205d30224ed5f\nminid.checksumMethod: sha1\nminid.status: ACTIVE\nminid.locations: http://bd2k.ini.usc.edu/assets/all-hands-meeting/minid_v0.1_Nov_2015.pdf\nminid.titles: minid: A BD2K Minimal Viable Identifier Pilot v0.1'

# internal anvl dict
ANVLdict = {'_target': "ark:/99999/fk4r8059v", \
        '_profile': 'minid', \
        '_status': 'reserved', \
        'minid.created': '2015-11-10 04:44:44.387671', \
        'minid.creator': "0000-0003-2129-5269", \
        'minid.checksum': "cacc1abf711425d3c554277a5989df269cefaa906d27f1aaa72205d30224ed5f", \
        'minid.checksumMethod': "sha1", \
        'minid.status': "ACTIVE", \
        'minid.locations': "http://bd2k.ini.usc.edu/assets/all-hands-meeting/minid_v0.1_Nov_2015.pdf", \
        'minid.titles': "minid: A BD2K Minimal Viable Identifier Pilot v0.1" \
        }

#==================================================================================#


class BasicTests():
    def test_objects_exist(self):
        self.assertIsNotNone(self.ANVL)
        self.assertIsNotNone(self.JSON)

    def test_read_json(self):
        self.assertIsNotNone(self.JSON.JSONdict)
        self.assertDictEqual(self.JSON.JSONdict, JSONdict)

    def test_read_anvl(self):
        self.assertIsNotNone(self.ANVL.ANVLdict)
        self.assertDictEqual(self.ANVL.ANVLdict, ANVLdict)

    def test_json_to_anvl(self):
        self.JSON.ANVLdict = None
        self.assertIsNone(self.JSON.ANVLdict)

        self.JSON.JSONtoANVL()
        self.assertIsNotNone(self.JSON.ANVLdict)
        self.assertDictEqual(self.JSON.ANVLdict, ANVLdict)

    def test_anvl_to_json(self):
        self.ANVL.JSONdict = None
        self.assertIsNone(self.ANVL.JSONdict)

        self.ANVL.ANVLtoJSON()
        self.assertIsNotNone(self.ANVL.JSONdict)
        self.assertDictEqual(self.ANVL.JSONdict, JSONdict)

    def test_objects_anvl_eq(self):
        self.JSON.JSONtoANVL()
        self.assertEqual(self.ANVL.ANVLdict, self.JSON.ANVLdict)

    def test_objects_json_eq(self):
        self.ANVL.ANVLtoJSON()
        self.assertEqual(self.ANVL.JSONdict, self.JSON.JSONdict)

    def test_return_anvl(self):
        # needs to be different when sent to EZID than when read in
        jsonANVL = self.JSON.returnANVL()
        anvlANVL = self.ANVL.returnANVL() 
        self.assertTrue(isinstance(jsonANVL, bytes))
        self.assertTrue(isinstance(anvlANVL, bytes))

    def test_return_json(self):
        jsonJSON = self.JSON.returnJSON()
        anvlJSON = self.ANVL.returnJSON() 
        self.assertTrue(isinstance(jsonJSON, str))
        self.assertTrue(isinstance(anvlJSON, str))
        self.assertEqual(json.loads(jsonJSON), json.loads(JSON))
        self.assertEqual(json.loads(anvlJSON), json.loads(JSON))


class MinidTest(unittest.TestCase, BasicTests):
    def setUp(self):
        self.JSON = Minid(ResponseText = JSON, Type = "JSON")
        self.ANVL = Minid(ResponseText = ANVL, Type = "ANVL")
        self.maxDiff = None

    def tearDown(self):
        pass

class DataCatalogTest(unittest.TestCase, BasicTests):
    def setUp(self):
        pass

    def tearDown(self):
        pass

if __name__=="__main__":
   unittest.main() 
