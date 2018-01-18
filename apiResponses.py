from flask import Response as flaskResponse
import requests

def buildResponse(ReqResponse, ContentType="text/plain"):
    '''Transfer requests response object into a flask Response object'''
    builtResponse = flaskResponse(
            status = ReqResponse.status_code,
            response = ReqResponse.content, 
            mimetype = ContentType 
            )
    return builtResponse 

# 401 Unauthorized
EmptyAuth = flaskResponse(
        response = 'Missing Login information, cannot use MDS without authentication',
        status = 401,
        mimetype = 'text/plain'
        )

#Create some different error response objects for flask
PostGet405 = flaskResponse( 
        response = 'Method Not Allowed: POST or GET at this Endpoint', 
        status = 405,
        mimetype = 'text/plain'
        )

Get405 = flaskResponse( 
        response = 'Method Not Allowed: Only GET at this Endpoint', 
        status = 405,
        mimetype = 'text/plain'
        )

GetDelete405 = flaskResponse( 
        response = 'Method Not Allowed: DELETE and GET at this Endpoint', 
        status = 405,
        mimetype = 'text/plain'
        )
