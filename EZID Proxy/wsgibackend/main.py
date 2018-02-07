from flask import Flask, render_template, request, Response 
import json
import requests
import re

def escape (s):
  return re.sub("[%:\r\n]", lambda c: "%%%02X" % ord(c.group(0)), s)

def CompressAnvl(Metadata): 
    return "\n".join("%s: %s" % (escape(name), escape(value)) for 
            name, value in Metadata.items()).encode("UTF-8")

def ParseGeneric(PassedDict):
    ''' 
        Take In the Passed Body, determine the type of Core Metadata
        parse and validate the requestBody

        Return an ANVL string, with fields correctly mapped to EZID metadata
    '''
    # Minid
    if set(PassedDict.keys()) == set(['identifier', 'created', 'creator', 'checksum', 'checksumMethod', 'status', 'locations', 'titles']):
        return ParseMinid(PassedDict)

    # DataCatalogue
    if set(PassedDict.keys()) == set(['@context', '@id', '@type', 'identifier', 'name']): 
        return ParseDataCataloge(PassedDict) 

    #DatasetUnpublished
    if set(PassedDict.keys()) == set(['@context', '@id', '@type', 'identifier', 'includedInDataCatalogue', 'dateCreated', 'distribution']): 
        return ParseDatasetUnpublished(PassedDict)

    #DatasetPublished
    if set(PassedDict.keys()) == set(['@context', '@id', '@type', 'identifier', 'includedInDataCatalogue', 'dateCreated', 'datePublished', 'distribution', 'author', 'name', 'description', 'keywords', 'version', 'citation']): 
        return ParseDatasetPublished(PassedDict)

    #DatasetDownload
    if set(PassedDict.keys()) ==  set(['@context', '@id', '@type', 'identifier','inDataset' , 'version', 'contentSize']): 
        return ParseDatasetDownload(PassedDict)

    # Return nothing/ throw error?
    else:
        return None

def ParseMinid(PassedDict):
    '''
        Parse JSON and translate into ANVL
    '''

    NewDict = {}

    NewDict['_profile'] = 'minid'
    NewDict['_status'] = 'reserved'

    NewDict['minid.created'] = PassedDict['created']
    NewDict['minid.creator'] = PassedDict['creator']
    NewDict['minid.checksum'] = PassedDict['checksum']
    NewDict['minid.checksumMethod'] = PassedDict['checksumMethod']
    NewDict['minid.status'] = PassedDict['status']
    NewDict['minid.locations'] = ";".join(PassedDict['locations'])
    NewDict['minid.titles'] = ";".join(PassedDict['titles'])

    url = "/".join(["https://ezid.cdlib.org/id",PassedDict['identifier']])
    return CompressAnvl(NewDict), url

def ParseDatasetUnpublished(PassedDict):
    ''' 
        Translate submitted keys into EZID fields
        Build a New Dictionary and Join into plaintext 

        Core Metadata Fields for DatasetUnpublished
        - identifier                -> _target
        - includedInDataCatalogue   -> NIHdc.dataCatalogue
        - dateCreated               -> NIHdc.dateCreated
        - distribution              -> NIHdc.distribution

        Filling in of EZID fields
        - _profile  : 'NIHdc'
        - _status   : 'reserved'
    '''
    NewDict = {} 

    NewDict['_profile'] = 'NIHdc'
    NewDict['_status'] = 'reserved'     
    NewDict['_target'] = PassedDict['identifier']

    NewDict['NIHdc.type'] = 'DatasetUnpublished'
    NewDict['NIHdc.dateCreated'] = PassedDict['dateCreated']
    NewDict['NIHdc.distribution'] = PassedDict['distribution']
    NewDict['NIHdc.includedInDataCatalogue'] = PassedDict['includedInDataCatalogue']

    url = "/".join(["https://ezid.cdlib.org/id",PassedDict['@id']])
    return CompressAnvl(NewDict), url

def ParseDatasetPublished(PassedDict):
    ''' 
        Translate submitted keys into EZID fields
        Build a New Dictionary and Join into plaintext 

       Core Metadata Fields for DatasetPublished
       - identifier              -> _target
       - includedInDataCatalogue -> NIHdc.dataCatalogue
       - dateCreated             -> NIHdc.dateCreated
       - datePublished           -> NIHdc.datePublished
       - distribution            -> NIHdc.distribution
       - author                  -> NIHdc.datasetAuthor
       - name                    -> NIHdc.datasetName
       - description             -> NIHdc.datasetDescription
       - keywords                -> NIHdc.datasetKeywords
       - version                 -> NIHdc.datasetVersion
       - citation                -> NIHdc.datasetCitation
    '''

    NewDict = {}
    NewDict['_profile'] = 'NIHdc'
    NewDict['_status'] = 'reserved' 
    NewDict['_target'] = PassedDict['identifier']

    NewDict['NIHdc.type'] = 'DatasetPublished'
    NewDict['NIHdc.includedInDataCatalogue'] = PassedDict['includedInDataCatalogue']
    NewDict['NIHdc.dateCreated'] = PassedDict['dateCreated']
    NewDict['NIHdc.datePublished'] = PassedDict['datePublished']
    NewDict['NIHdc.distribution'] = PassedDict['distribution']
    NewDict['NIHdc.author'] = PassedDict['author']
    NewDict['NIHdc.name'] = PassedDict['name']
    NewDict['NIHdc.description'] = PassedDict['description']
    NewDict['NIHdc.keywords'] = PassedDict['keywords']
    NewDict['NIHdc.version'] = PassedDict['version']
    NewDict['NIHdc.citation'] = PassedDict['citation']

    url = "/".join(["https://ezid.cdlib.org/id",PassedDict['@id']])
    return CompressAnvl(NewDict), url

def ParseDatasetDownload(PassedDict):
    ''' Translate submitted keys into EZID fields
        Build a New Dictionary and Join into plaintext 

       Core Metadata Fields for DatasetPublished
       - identifier  -> _target                 (download link)
       *- dataset     -> NIHdc.downloadParent     (GUID for dataset)*
       - version     -> NIHdc.downloadVersion   (fingerprint)
       - contextSize -> NIHdc.downloadSize      (file size)
        
    '''
    NewDict = {}

    NewDict['_profile'] = 'NIHdc'
    NewDict['_status'] = 'reserved' 

    NewDict['NIHdc.type'] = 'DatasetDownload'
    NewDict['NIHdc.inDataset'] = PassedDict['inDataset']
    NewDict['NIHdc.version'] = PassedDict['version']
    NewDict['NIHdc.contentSize'] =   PassedDict['contentSize']

    url = "/".join(["https://ezid.cdlib.org/id",PassedDict['@id']])
    return CompressAnvl(NewDict), url

def ParseDataCataloge(PassedDict):
    ''' Translate submitted keys into EZID fields
        Build a New Dictionary and Join into plaintext 

        Mapping of requestBody attributes
        - identifier->      _target
        - @context  ->      NIHdc.context
        - @type     ->      NIHdc.type
        - name      ->      NIHdc.name

        Filling in of EZID fields
        - _profile  : 'NIHdc'
        - _status   : 'reserved'
    '''
    NewDict = {}

    NewDict['_profile'] = 'NIHdc' 
    NewDict['_status'] = 'reserved'
    NewDict['_target'] = PassedDict['identifier']

    NewDict['NIHdc.type'] = 'DataCatalogue'
    NewDict['NIHdc.context'] = PassedDict['@context']
    NewDict['NIHdc.type'] = PassedDict['@type'] 
    NewDict['NIHdc.name'] = PassedDict['name']

    url = "/".join(["https://ezid.cdlib.org/id",PassedDict['@id']])
    return CompressAnvl(NewDict), url

def ChompAnvl(PlainText):
    '''
        Taking a PlainText response body and parsing it into JSON-LD
    '''
    NewDict = {}
    if isinstance(PlainText, bytes):
        PlainText = str(PlainText, 'UTF-8')

    for element in PlainText.split("\n"):
        SplitUp = element.split(": ")
        if len(SplitUp)>1:
            NewDict[SplitUp[0]] = SplitUp[1]
    return NewDict


def ParseJSONLD(ResponseContent, ID):
    '''
        Digests the EZID Response body and rebuilds the JSON-LD body

        For _profile == NIHdc
            Every Body 
                _@context = "http://schema.org"
            
            Consistent Mapping
                ID      -> @id  
                _target -> identifier

    '''
    RawDictionary = ChompAnvl(ResponseContent)
    MappingDictionary = {}

    if RawDictionary['_profile'] == 'minid': 
        MappingDictionary['identifier'] = RawDictionary['_target']
        MappingDictionary['created'] = RawDictionary['minid.created']
        MappingDictionary['creator'] = RawDictionary['minid.creator'] 
        MappingDictionary['checksum'] = RawDictionary['minid.checksum']
        MappingDictionary['checksumMethod'] = RawDictionary['minid.checksumMethod']
        MappingDictionary['status'] = RawDictionary['minid.status']
        MappingDictionary['locations'] = RawDictionary['minid.locations'].split(";")
        MappingDictionary['titles'] = RawDictionary['minid.titles'].split(";")
        ResponseType = 'minid'

    if RawDictionary['_profile'] == 'NIHdc':
        MappingDictionary['@context'] = "http://schema.org"
        MappingDictionary['@id'] = ID
        MappingDictionary['identifier'] = RawDictionary['_target']
        MappingDictionary['@type'] = RawDictionary['NIHdc.type']
        
        if MappingDictionary['@type'] == 'DataCatalogue':
            MappingDictionary['name'] = RawDictionary['NIHdc.name']
            ResponseType = 'DataCatalogue'

        if MappingDictionary['@type'] == 'DatasetUnpublished':
            MappingDictionary['includedInDataCatalogue'] = RawDictionary['NIHdc.includedInDataCatalogue']
            MappingDictionary['dateCreated'] = RawDictionary['NIHdc.dateCreated']
            MappingDictionary['distribution'] = RawDictionary['NIHdc.distribution']
            ResponseType = 'DatasetUnpublished'

        if MappingDictionary['@type']  == 'DatasetPublished':
            MappingDictionary['includedInDataCatalogue'] = RawDictionary['NIHdc.includedInDataCatalogue']
            MappingDictionary['dateCreated'] = RawDictionary['NIHdc.dateCreated']
            MappingDictionary['datePublished'] = RawDictionary['NIHdc.datePublished']
            MappingDictionary['distribution'] = RawDictionary['NIHdc.distribution']
            MappingDictionary['author'] = RawDictionary['NIHdc.author']
            MappingDictionary['name'] = RawDictionary['NIHdc.name']
            MappingDictionary['description'] = RawDictionary['NIHdc.description']
            MappingDictionary['keywords'] = RawDictionary['NIHdc.keywords']
            MappingDictionary['version'] = RawDictionary['NIHdc.version']
            MappingDictionary['citation'] = RawDictionary['NIHdc.citation']
            ResponseType = 'DatasetPublished'
            
        if MappingDictionary['@type']  == 'DatasetDownload':
            MappingDictionary['inDataset'] = RawDictionary['NIHdc.inDataset']
            MappingDictionary['version'] = RawDictionary['NIHdc.version']
            MappingDictionary['contentSize'] = RawDictionary['NIHdc.contentSize']
            ResponseType = 'DatasetDownload'
 
    return MappingDictionary, ResponseType

def RenderLandingPage(ResponseContent, ID):
    Payload, ResponseType = ParseJSONLD(ResponseContent, ID)
    if ResponseType == 'minid':
        return render_template('minid.html', Payload=Payload)
    if ResponseType == 'DataCatalogue':
        return render_template('dataCatalogue.html', Payload=Payload)
    if ResponseType == 'DatasetUnpublished':
        return render_template('datasetUnpublished.html', Payload=Payload)
    if ResponseType == 'DatasetPublished':
        return render_template('datasetPublished.html', Payload=Payload)
    if ResponseType == 'DatasetDownload':
        return render_template('dataDownload.html', Payload=Payload)

app = Flask('EZIDwraper')
app.config['Debug'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = False
app.config['Testing'] = False

EmptyAuth = Response(
        response = 'Missing Login information, cannot mint/updates IDs without authentication',
        status = 401,
        mimetype = 'text/plain'
        )

NoID = Response(
            status = 404,
            response = "No record of this Identifier was found",
            mimetype = "text/plain"
        )

EmptyBody = Response(
            status = 400,
            response = "You need to submit a request body",
            mimetype = 'text/plain'
        )

BadRequestBody = Response(
            status = 400,
            response = "Submitted Request Body was missing required parameters",
            mimetype = 'text/plain'
        )

MethodNotAllowed = Response(
            status = 405,
            response = "Method Not Supported, either PUT or GET",
            mimetype = 'text/plain'
        )

UnfinishedBuisness = Response(
        status = 501,
        response = "Not Yet Built, Working On It!",
        mimetype = 'text/plain'
        )

def buildResponse(ReqResponse, ContentType="text/plain"):
    '''Transfer requests response object into a flask Response object'''
    return Response( status = ReqResponse.status_code, \
            response = ReqResponse.content, \
            mimetype = ContentType )


@app.route('/minid/mint', methods = ['PUT'])
def mintID():   
    headers = {'Content-Type': 'text/plain; charset=UTF-8'}
    passedAuth = request.authorization

    if request.method == 'PUT':

        if not passedAuth or not passedAuth.password or not passedAuth.username:
            return EmptyAuth 

        BasicAuth = requests.auth.HTTPBasicAuth(passedAuth.username, passedAuth.password)
        payload = request.get_json()

        if not (payload):
            return EmptyBody

        ParsedBody, url =  ParseGeneric(payload)
        if ParsedBody: 
            response = requests.put(
                            url,
                            auth = BasicAuth,
                            headers= headers, 
                            data = ParsedBody)
            return buildResponse(response)

        else:
            return BadRequestBody

@app.route('/minid/<path:ID>', methods=['GET', 'DELETE'])
def runId(ID):

    headers = {'Content-Type': 'text/plain; charset=UTF-8'}
    url = "/".join(["https://ezid.cdlib.org/id",ID])
    passedAuth = request.authorization

    if request.method == 'GET': 
        response = requests.get(url)

        if response.status_code == 200: 
            # JSON-LD in the schema.org profile
            if request.headers['Accept'] == 'application/ld+json':
                Dictionary, ContentType = ParseJSONLD(response.content, ID)
                return Response( status = 200,
                mimetype = 'application/ld+json; profile="http://schema.org"',  
                response = json.dumps(Dictionary)
                )

            # if text/html render a landing page
            if request.headers['Accept'] == 'text/html':
                return RenderLandingPage(response.content, ID)

            # if text/plain return EZID plaintext response
                # return buildResponse(response)

            # return a citation format
            if request.headers['Accept'] == 'text/x-bibliography':
                return UnfinishedBuisness

            else:
                return RenderLandingPage(response.content, ID)
 
        # TK: check response status, if it doesn't exist will cause errors
            # BE MORE PRECISE: read the plaintext errors
        if response.status_code == 400:
            return NoID

        else:
            return RenderLandingPage(response.content, ID)


    if request.method == 'DELETE':

        if not request.authorization or not request.authorization.password or not request.authorization.username:
            return EmptyAuth 

        BasicAuth = requests.auth.HTTPBasicAuth(passedAuth.username, passedAuth.password)
        response = requests.delete(url, auth=BasicAuth)
        return buildResponse(response)

    else:
        return MethodNotAllowed 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
