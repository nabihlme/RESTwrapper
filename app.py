# To run FLASK_APP=app.py flask run
# need to specify port in command for Docker

from flask import Flask, request, Response
from functools import wraps
import requests

app = Flask('DataCiteREST')
app.config['Debug'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['Testing'] = True

#########################
# DataCite REST
########################

#Create some different error response objects for flask
#405response = Response(
#            'Method Not Allowed.\n'
#            'Post or Get at this Endpoint', 405,
#            {'WWW-Authenticate': 'Basic realm="Login Required"'})



@app.route('/data-centers')
def listDataCenters():
    include = {'include':request.args.get('include')}
    response = requests.get("https://api.datacite.org/data-centers/", 
                            params=include)
    # include control flow for response.status_code
    return response.content

@app.route('/data-centers/<DataCenterID>')
def getDataCenter(DataCenterID):
    url = "/".join(["https://api.datacite.org/data-centers/", DataCenterID])
    response = requests.get(url)
    return response.content

@app.route('/members')
def listMembers():
    response = requests.get("https://api.datacite.org/members/")
    return response.content

@app.route('/members/<MemberID>')
def getMember(MemberID):
    url = "/".join(["https://api.datacite.org/members/", MemberID])
    response = requests.get(url)
    return response.content

@app.route('/contributors')
def getPerson():
    response = requests.get("https://api.datacite.org/contributors/")
    return response.content

@app.route('/people/<PersonID>')
def listPeople(PersonID):
    url = "/".join(["https://api.datacite.org/person", PersonID])
    response = requests.get(url)
    return response.content

@app.route('/works/<path:DOI>')
def getDOI(DOI):
    url = "/".join(["https://api.datacite.org/works", DOI])
    response = requests.get(url)
    return response.content

@app.route('/works')
def listWorks():
    response = requests.get("https://api.datacite.org/works")
    return response.content

#####################
# DataCite MDS
#####################

@app.route('/metadata', methods=['GET', 'POST'])
def requestMetadata():
    passedAuth = request.authorization

    #check if authorization exists

    if request.method == 'GET':
        response = requests.get('https://mds.test.datacite.org/metadata',
                    auth = requests.auth.HTTPBasicAuth(passedAuth.username, passedAuth.password))
    if request.method == 'POST':
        # get the passed metadata XML file
        metadata = request.data['xml']

        response = requests.get('https://mds.test.datacite.org/metadata',
                    auth = requests.auth.HTTPBasicAuth(passedAuth.username, passedAuth.password),
                    data = metadata.encode('utf-8'),
                    headers = {'Content-Type': 'application/xml;charset=UTF-8'})
    else:
        response = None 
    return response.content

@app.route('/doi', methods=['GET', 'POST'])
def requestDOI():
    passedAuth = request.authorization

    if request.method == 'GET':
        response = requests.get("https://mds.test.datacite.org/doi", 
                    auth = requests.auth.HTTPBasicAuth(passedAuth.username, passedAuth.password) )

    if request.method == 'POST':
        metadata = request.data['xml']
        response = requests.post("https://mds.test.datacite.org/doi",
                    auth = requests.auth.HTTPBasicAuth(passedAuth.username, passedAuth.password),
                    data = metadata.encode('utf-8'),
                    headers = {'Content-Type': 'application/xml;charset=UTF-8'})
    else:
        response = None
    return response.content

@app.route('/doi')
def getDOI():
    passedAuth = request.authorization

    response = requests.get("https://mds.test.datacite.org/doi",
                auth = requests.auth.HTTPBasicAuth(passedAuth.username, passedAuth.password))
            
    return response.content

@app.route('/media/<path:DOI>', methods=['GET', 'POST'])
def getMedia(DOI):
    passedAuth = request.authorization
    endpoint = "/".join(["https://mds.test.datacite.org/media", DOI])

    if request.method == 'GET':
        response = requests.get(endpoint,
                    auth = requests.auth.HTTPBasicAuth(passedAuth.username, passedAuth.password) )

    if request.method == 'POST':
        # get the media file
        metadata = request.data['text'] # how to get the data cleanly

        response = requests.post(endpoint,
                    auth = requests.auth.HTTPBasicAuth(passedAuth.username, passedAuth.password),
                    data = metadta.encode('utf-8'),
                    headers = {'Content-Type':'text/plain;charset=UTF-8'})
    else:
        response = None
    return response.content


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
