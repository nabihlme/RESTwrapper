# To run FLASK_APP=app.py flask run
# need to specify port in command for Docker

from flask import Flask, request, Response
import requests
from apiResponses import *

app = Flask('DataCiteREST')
app.config['Debug'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['Testing'] = True

#########################
# DataCite REST
########################

@app.route('/data-centers')
def listDataCenters():
    include = {'include':request.args.get('include')}
    response = requests.get("https://api.datacite.org/data-centers/", 
                            params=include)
    # include control flow for response.status_code
    return buildResponse(response)

@app.route('/data-centers/<DataCenterID>')
def getDataCenter(DataCenterID):
    url = "/".join(["https://api.datacite.org/data-centers/", DataCenterID])
    response = requests.get(url)
    return buildResponse(response)

@app.route('/members')
def listMembers():
    response = requests.get("https://api.datacite.org/members/")
    return buildResponse(response)

@app.route('/members/<MemberID>')
def getMember(MemberID):
    url = "/".join(["https://api.datacite.org/members/", MemberID])
    response = requests.get(url)
    return buildResponse(response)

@app.route('/contributors')
def getPerson():
    response = requests.get("https://api.datacite.org/contributors/")
    return buildResponse(response)

@app.route('/people/<PersonID>')
def listPeople(PersonID):
    url = "/".join(["https://api.datacite.org/person", PersonID])
    response = requests.get(url)
    return buildResponse(response)

@app.route('/works/<path:DOI>')
def getWork(DOI):
    url = "/".join(["https://api.datacite.org/works", DOI])
    response = requests.get(url)
    return buildResponse(response)

@app.route('/works')
def listWorks():
    response = requests.get("https://api.datacite.org/works")
    return buildResponse(response)

#####################
# DataCite MDS
#####################

@app.route('/metadata', methods=['GET', 'POST'])
def listMetadata():
    passedAuth = request.authorization

    if not passedAuth.password or not passedAuth.username:
        return EmptyAuth

    if request.method == 'GET':
        response = requests.get('https://mds.test.datacite.org/metadata',
                    auth = requests.auth.HTTPBasicAuth(passedAuth.username, passedAuth.password))
        return buildResponse(response)

    if request.method == 'POST':
        # get the passed metadata XML file
        metadata = request.data['xml']

        response = requests.post('https://mds.test.datacite.org/metadata',
                    auth = requests.auth.HTTPBasicAuth(passedAuth.username, passedAuth.password),
                    data = metadata.encode('utf-8'),
                    headers = {'Content-Type': 'application/xml;charset=UTF-8'})

        return buildResponse(response)
    
    else:
        return PostGet405

@app.route('/doi', methods=['GET', 'POST'])
def requestDOI():
    passedAuth = request.authorization

    if not passedAuth.password or not passedAuth.username:
        return EmptyAuth

    if request.method == 'GET':
        response = requests.get("https://mds.test.datacite.org/doi", 
                    auth = requests.auth.HTTPBasicAuth(passedAuth.username, passedAuth.password) )
        return buildResponse(response)

    if request.method == 'POST':
        metadata = request.data['xml']
        response = requests.post("https://mds.test.datacite.org/doi",
                    auth = requests.auth.HTTPBasicAuth(passedAuth.username, passedAuth.password),
                    data = metadata.encode('utf-8'),
                    headers = {'Content-Type': 'application/xml;charset=UTF-8'}) 
        return buildResponse(response)

    else:
        return PostGet405

@app.route('/doi')
def getDOI():
    passedAuth = request.authorization

    if not passedAuth.password or not passedAuth.username:
        return EmptyAuth
    
    print(request.authorization)

    response = requests.get("https://mds.test.datacite.org/doi",
                auth = requests.auth.HTTPBasicAuth(passedAuth.username, passedAuth.password))
            
    return buildResponse(response)

@app.route('/media/<path:DOI>', methods=['GET', 'POST'])
def getMedia(DOI):
    passedAuth = request.authorization

    if not passedAuth.password or not passedAuth.username:
        return EmptyAuth

    endpoint = "/".join(["https://mds.test.datacite.org/media", DOI])

    if request.method == 'GET':
        response = requests.get(endpoint,
                    auth = requests.auth.HTTPBasicAuth(passedAuth.username, passedAuth.password) )
        return buildResponse(response)

    if request.method == 'POST':
        # get the media file
        metadata = request.data['text'] # how to get the data cleanly

        response = requests.post(endpoint,
                    auth = requests.auth.HTTPBasicAuth(passedAuth.username, passedAuth.password),
                    data = metadta.encode('utf-8'),
                    headers = {'Content-Type':'text/plain;charset=UTF-8'})
        return buildResponse(response)

    else:
        return PostGet405

@app.route('/metadata/<path:DOI>', methods=['GET', 'DELETE'])
def lookupMetadata(DOI):
    passedAuth = request.authorization

    if not passedAuth.password or not passedAuth.username:
        return EmptyAuth

    endpoint = "/".join(["https://mds.test.datacite.org/media", DOI])

    if request.method == 'GET':
        response = requests.get(endpoint,
                        auth = requests.auth.HTTPBasicAuth(passedAuth.username, passedAuth.password) )
        return buildResponse(response)

    if request.method == 'DELETE':
        response = requests.delete(endpoint,
                        auth = requests.auth.HTTPBasicAuth(passedAuth.username, passedAuth.password) )
        return buildResponse(response)

    else:
        return GetDelete405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
