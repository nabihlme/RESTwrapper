import json
import re

def escape (s):
  return re.sub("[%:\r\n]", lambda c: "%%%02X" % ord(c.group(0)), s)

class BodyResponse(object):
    def __init__(self, ResponseText, Type):
        assert Type == "ANVL" or Type == "JSON"
        self.ANVLdict = None
        self.JSONdict = None

        if Type == "ANVL":
            self.digestANVL(ResponseText)

        if Type == "JSON":
            self.JSONdict = json.loads(ResponseText)


    def digestANVL(self, ResponseText): 
        self.ANVLdict = {}
        tempANVL = ResponseText.decode('UTF-8')

        for element in tempANVL.split("\n"):
            SplitUp = element.split(": ", 1)
            if len(SplitUp)>1:
                self.ANVLdict[SplitUp[0]] = SplitUp[1] 

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
        self.ANVLdict['_target'] = self.JSONdict['identifier']
        self.ANVLdict['minid.created'] = self.JSONdict['created']
        self.ANVLdict['minid.creator'] = self.JSONdict['creator']
        self.ANVLdict['minid.checksum'] = self.JSONdict['checksum']
        self.ANVLdict['minid.checksumMethod'] = self.JSONdict['checksumMethod']
        self.ANVLdict['minid.status'] = self.JSONdict['status']
        self.ANVLdict['minid.locations'] = ";".join(self.JSONdict['locations'])
        self.ANVLdict['minid.titles'] = ";".join(self.JSONdict['titles'])

        self.EZIDurl = "/".join(["https://ezid.cdlib.org/id",self.JSONdict['identifier']])

            
class DataCatalog(BodyResponse):
    
    def JSONtoANVL(self):
        assert self.JSONdict is not None
        assert self.ANVLdict is None

        self.ANVLdict = {}

        self.AVNLdict['_profile'] = 'NIHdc'
        self.ANVLdict['_status'] = 'reserved'

        self.ANVLdict['_target'] = self.JSONdict['@id']
        self.ANVLdict['NIHdc.identifier'] = self.JSONdict['identifier']
        self.ANVLdict['NIHdc.name'] = self.JSONdict['name']
        self.ANVLdict['NIHdc.description'] = self.JSONdict['description']

    def ANVLtoJSON():
        assert self.ANVLdict is not None
        assert self.JSONdict is None
        self.JSONdict = {}

        self.JSONdict['@id'] = self.ANVLdict['_target']
        self.JSONdict['identifier'] = self.ANVLdict['NIHdc.identifier']
        self.JSONdict['name'] = self.ANVLdict['NIHdc.name']
        self.JSONdict['description'] = self.ANVLdict['NIHdc.description']
        


class Dataset(BodyResponse):

    def JSONtoANVL():
        pass

    def ANVLtoJSON():
        pass


class DataDownload(BodyResponse):

    def JSONtoANVL():
        pass

    def ANVLtoJSON():
        pass

