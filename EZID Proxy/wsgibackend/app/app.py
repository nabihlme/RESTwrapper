from flask import Flask, render_template, request, Response 
import json
import requests
import re
from components.objects import *
from components.responses import *


def RenderLandingPage(ResponsePayload):
    '''
        Pass the Response Payload object, 
        determine the appropriate template
        Render, and Return
    '''
    if isinstance(ResponsePayload, Minid):
        return render_template('minid.html', Payload=ResponsePayload.JSONdict)
    if isinstance(ResponsePayload, DataCatalog):
        return render_template('datasetCatalog.html', Payload=ResponsePayload.JSONdict)
    if isinstance(ResponsePayload, Dataset):
        return render_template('dataset.html', Payload=ResponsePayload.JSONdict)
    if isinstance(ResponsePayload, DataDownload):
        return render_template('dataDownload.html', Payload=ResponsePayload.JSONdict)

app = Flask('EZIDwraper')
app.config['Debug'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = False
app.config['Testing'] = False

@app.route('/minid/mint', methods = ['PUT'])
def mintID():   
    headers = {'Content-Type': 'text/plain; charset=UTF-8'}

    passedAuth = None # if doesn't exist will trigger NameError at if not
    passedAuth = request.authorization

    if request.method == 'PUT':

        if not passedAuth or not passedAuth.password or not passedAuth.username:
            return EmptyAuth 

        BasicAuth = requests.auth.HTTPBasicAuth(passedAuth.username, passedAuth.password)

        payload = None # if doesn't exist will trigger NameError at if not
        payload = request.get_json()

        if not (payload):
            return EmptyBody

        ANVLsubmission = None
        ANVLsubmission = PayloadFactory(payload, "JSON")
        ANVLsubmission.JSONtoANVL()
        
        print(ANVLsubmission.URL)

        if ANVLsubmission: 
            response = requests.put(
                            url=ANVLsubmission.URL,
                            auth = BasicAuth,
                            headers= headers, 
                            data = ANVLsubmission.returnANVL() )
            return buildResponse(response)

        else:
            return BadRequestBody

@app.route('/minid/<path:ID>', methods=['GET', 'DELETE'])
def runId(ID):

    headers = {'Content-Type': 'text/plain; charset=UTF-8'}
    url = "/".join(["https://ezid.cdlib.org/id",ID])
    
    passedAuth = None
    passedAuth = request.authorization

    if request.method == 'GET': 
        response = requests.get(url)
        

        if response.status_code == 200:  
            ANVLResponse = PayloadFactory(response.content, "ANVL")
            ANVLResponse.ANVLtoJSON()

            # JSON-LD in the schema.org profile
            if request.headers['Accept'] == 'application/ld+json':
                return Response( status = 200,
                mimetype = 'application/ld+json; profile="http://schema.org"',  
                response = ANVLResponse.returnJSON()               
                )

            # if text/html render a landing page
            if request.headers['Accept'] == 'text/html':
                return RenderLandingPage(ANVLResponse)

            # if text/plain return EZID plaintext response
                # return buildResponse(response)

            # return a citation format
            if request.headers['Accept'] == 'text/x-bibliography':
                return UnfinishedBuisness

            else:
                return RenderLandingPage(ANVLResponse)
 
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
