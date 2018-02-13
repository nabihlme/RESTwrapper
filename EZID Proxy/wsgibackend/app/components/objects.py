import json
import re

EZID = "https://ezid.cdlib.org/id/"

def escape (s):
  return re.sub("[%:\r\n]", lambda c: "%%%02X" % ord(c.group(0)), s)


def digestANVL(ResponseText): 
    ANVLdict = {}
    if isinstance(ResponseText, bytes):
        tempANVL = ResponseText.decode('UTF-8')
    else:
        tempANVL = ResponseText

    for element in tempANVL.split("\n"):
        SplitUp = element.split(": ", 1)
        if len(SplitUp)>1:
            ANVLdict[SplitUp[0]] = SplitUp[1] 

    return ANVLdict


def PayloadFactory(ResponseText, Type):
    '''
        Factory Pattern, returns the appropriate object
        Need to be able to pass already parsed dictionaries, some optional arguments
        Currently runs digestANVL twice 
    '''
    if Type=="ANVL":
        tempDict = digestANVL(ResponseText) 
        if set(['_target','minid.created','minid.creator','minid.checksum','minid.checksumMethod', \
                'minid.status', 'minid.locations', 'minid.titles']).issubset(set(tempDict.keys())):
            return Minid(ResponseText, "ANVL")
        if set(['_target', 'NIHdc.identifier', 'NIHdc.name', 'NIHdc.description']).issubset(set(tempDict.keys())):
            return DataCatalog(ResponseText, "ANVL")
        if set(['_target', 'NIHdc.identifier', 'NIHdc.includedInDataCatalog','NIHdc.dateCreated']).issubset(set(tempDict.keys())):
            return Dataset(ResponseText, "ANVL")
        if set(['_target', 'NIHdc.identifier', 'NIHdc.version', 'NIHdc.contentSize', 'NIHdc.fileFormat', \
                'NIHdc.contentUrl']).issubset(set(tempDict.keys())):
            return DataDownload(ResponseText, "ANVL")

    if Type=="JSON":
        # need to also set the URL without converting

        if isinstance(ResponseText, dict):
            tempDict = ResponseText
        else:
            tempDict = json.loads(ResponseText)

        if set(['identifier', 'created', 'creator', 'checksum','checksumMethod','status','locations', \
                'titles']).issubset(tempDict.keys()):
            return Minid(ResponseText, "JSON")
        if set(['@id', 'identifier', 'name', 'description']).issubset(set(tempDict.keys())):
            return DataCatalog(ResponseText, "JSON")
        if set(['@id', 'identifier', 'includedInDataCatalog', 'dateCreated']).issubset(set(tempDict.keys())):
            return Dataset(ResponseText, "JSON")
        if set(['@id', 'identifier', 'version', 'contentSize', 'fileFormat', 'contentUrl']).issubset(set(tempDict.keys())):
            return DataDownload(ResponseText, "JSON")

class BodyResponse(object):
    def __init__(self, ResponseText, Type):
        assert Type == "ANVL" or Type == "JSON"
        self.ANVLdict = None
        self.URL = None
        self.JSONdict = None

        if Type == "ANVL":
            self.ANVLdict = self.digestANVL(ResponseText)
            # minid 

        if Type == "JSON":
            if isinstance(ResponseText, dict):
                self.JSONdict = ResponseText
            else:
                self.JSONdict = json.loads(ResponseText)

    def digestANVL(self, ResponseText): 
        ANVLdict = {}
        if isinstance(ResponseText, bytes):
            tempANVL = ResponseText.decode('UTF-8')
        else:
            tempANVL = ResponseText

        for element in tempANVL.split("\n"):
            SplitUp = element.split(": ", 1)
            if len(SplitUp)>1:
                ANVLdict[SplitUp[0]] = SplitUp[1] 

        return ANVLdict

    def returnANVL(self):
        if self.ANVLdict is None:
            self.JSONtoANVL()

        return "\n".join("%s: %s" % (escape(name), escape(value)) for \
                name, value in self.ANVLdict.items()).encode("UTF-8")
    
    def returnJSON(self):
        if self.JSONdict is None:
            self.ANVLtoJSON()

        return json.dumps(self.JSONdict)

class Minid(BodyResponse):

    def ANVLtoJSON(self):
        ''' 
            Convert the ANVLdict to the JSONdict 
                Describing the Mapping
                _target         ->      identifier
                minid.created   ->      created
                minid.creator   ->      creator
                minid.checksum  ->      checksum
                minid.checksumMethod -> checksumMethod
                minid.status    ->      status
                minid.locations ->      locations
                minid.titles    ->      titles
        '''
        self.JSONdict = {}
        self.JSONdict['identifier'] = self.ANVLdict['_target']
        self.JSONdict['created'] = self.ANVLdict['minid.created']
        self.JSONdict['creator'] = self.ANVLdict['minid.creator']
        self.JSONdict['checksum'] = self.ANVLdict['minid.checksum']
        self.JSONdict['checksumMethod'] = self.ANVLdict['minid.checksumMethod']
        self.JSONdict['status'] = self.ANVLdict['minid.status']
        self.JSONdict['locations'] = list(self.ANVLdict['minid.locations'].split(";"))
        self.JSONdict['titles'] = list(self.ANVLdict['minid.titles'].split(";"))


    def JSONtoANVL(self):
        ''' 
            Conver the ANVLdict to the JSONdict 
                Setting EZID metadata
                    _profile = minid
                    _status  = reserved

                Describing the Mapping
                    created         -> minid.created
                    creator         -> minid.creator
                    checksum        -> minid.checksum
                    checksumMethod  -> minid.checksumMethod
                    status          -> minid.status
                    locations       -> minid.locations
                    titles          -> minid.titles
        '''
        self.ANVLdict = {}
        self.ANVLdict['_profile'] = 'minid'
        self.ANVLdict['_status'] = 'reserved'
        #self.ANVLdict['_target'] = self.JSONdict['identifier']
        self.ANVLdict['minid.created'] = self.JSONdict['created']
        self.ANVLdict['minid.creator'] = self.JSONdict['creator']
        self.ANVLdict['minid.checksum'] = self.JSONdict['checksum']
        self.ANVLdict['minid.checksumMethod'] = self.JSONdict['checksumMethod']
        self.ANVLdict['minid.status'] = self.JSONdict['status']
        self.ANVLdict['minid.locations'] = ";".join(self.JSONdict['locations'])
        self.ANVLdict['minid.titles'] = ";".join(self.JSONdict['titles'])

        # need to know where to send payload
        self.URL = "".join([EZID, self.JSONdict['identifier'] ])
            
class DataCatalog(BodyResponse):
 
    def JSONtoANVL(self):
        assert self.JSONdict is not None
        assert self.ANVLdict is None

        self.ANVLdict = {}

        self.ANVLdict['_profile'] = 'NIHdc'
        self.ANVLdict['_status'] = 'reserved'

        #self.ANVLdict['_target'] = self.JSONdict['@id']
        self.ANVLdict['NIHdc.identifier'] = self.JSONdict['identifier']
        self.ANVLdict['NIHdc.name'] = self.JSONdict['name']
        self.ANVLdict['NIHdc.description'] = self.JSONdict['description']

        self.URL = "".join([EZID, self.JSONdict['@id'] ])

    def ANVLtoJSON(self):
        assert self.ANVLdict is not None
        assert self.JSONdict is None
        self.JSONdict = {}
    
        self.JSONdict['@context'] = 'http://schema.org'
        self.JSONdict['@id'] = self.ANVLdict['_target']
        self.JSONdict['identifier'] = self.ANVLdict['NIHdc.identifier']
        self.JSONdict['name'] = self.ANVLdict['NIHdc.name']
        self.JSONdict['description'] = self.ANVLdict['NIHdc.description']
        

class Dataset(BodyResponse):

    def JSONtoANVL(self):
        assert self.JSONdict is not None
        assert self.ANVLdict is None

        self.ANVLdict = {}

        self.ANVLdict['_profile'] = 'NIHdc'
        self.ANVLdict['_status'] = 'reserved'

        #self.ANVLdict['_target'] = self.JSONdict['@id']
        self.ANVLdict['NIHdc.identifier'] = self.JSONdict['identifier']
        self.ANVLdict['NIHdc.includedInDataCatalog'] = self.JSONdict['includedInDataCatalog']
        self.ANVLdict['NIHdc.dateCreated'] = self.JSONdict['dateCreated']

        self.URL = "".join([EZID, self.JSONdict['@id'] ])

    def ANVLtoJSON(self):
        assert self.ANVLdict is not None
        assert self.JSONdict is None
        self.JSONdict = {}
    
        self.JSONdict['@context'] = 'http://schema.org'
        self.JSONdict['@id'] = self.ANVLdict['_target']
        self.JSONdict['identifier'] = self.ANVLdict['NIHdc.identifier']
        self.JSONdict['includedInDataCatalog'] = self.ANVLdict['NIHdc.includedInDataCatalog']
        self.JSONdict['dateCreated'] = self.ANVLdict['NIHdc.dateCreated']


class DataDownload(BodyResponse):

    def JSONtoANVL(self):
        assert self.JSONdict is not None
        assert self.ANVLdict is None

        self.ANVLdict = {}

        self.ANVLdict['_profile'] = 'NIHdc'
        self.ANVLdict['_status'] = 'reserved'

        #self.ANVLdict['_target'] = self.JSONdict['@id']
        self.ANVLdict['NIHdc.identifier'] = self.JSONdict['identifier']
        self.ANVLdict['NIHdc.version'] = self.JSONdict['version']
        self.ANVLdict['NIHdc.contentSize'] = self.JSONdict['contentSize']
        self.ANVLdict['NIHdc.fileFormat'] = self.JSONdict['fileFormat']
        self.ANVLdict['NIHdc.contentUrl'] = self.JSONdict['contentUrl']

        self.URL = "".join([EZID, self.JSONdict['@id'] ])

    def ANVLtoJSON(self):
        assert self.ANVLdict is not None
        assert self.JSONdict is None
        self.JSONdict = {}
   
        self.JSONdict['@context'] = 'http://schema.org'
        self.JSONdict['@id'] = self.ANVLdict['_target']
        self.JSONdict['identifier'] = self.ANVLdict['NIHdc.identifier'] 
        self.JSONdict['version'] = self.ANVLdict['NIHdc.version']
        self.JSONdict['contentSize'] = self.ANVLdict['NIHdc.contentSize'] 
        self.JSONdict['fileFormat'] = self.ANVLdict['NIHdc.fileFormat']
        self.JSONdict['contentUrl'] = self.ANVLdict['NIHdc.contentUrl']

