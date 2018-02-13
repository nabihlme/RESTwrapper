from flask import Response

EmptyAuth = Response(
        status = 401,
        response = '{"error": {"description": "Missing Login information, cannot mint/updates IDs without authentication"}]}',
        mimetype = 'application/ld+json'
        )

NoID = Response(
            status = 404,
            response = '{"error":"No record of this Identifier was found"}',
            mimetype = 'application/ld+json'
        )

EmptyBody = Response(
            status = 400,
            response = '{"error":"You need to submit a request body"}',
            mimetype = 'application/ld+json'
        )

BadRequestBody = Response(
            status = 400,
            response = '{"error": "Submitted Request Body was missing required parameters"}',
            mimetype = 'application/ld+json'
        )

MethodNotAllowed = Response(
            status = 405,
            response = '{"error": "Method Not Supported, either PUT or GET"}',
            mimetype = 'application/ld+json'
        )

UnfinishedBuisness = Response(
        status = 501,
        response = '{"error":"Not Yet Built, Working On It!"}',
        mimetype = 'application/ld+json'
        )

def buildResponse(ReqResponse, ContentType="text/plain"):
    '''Transfer requests response object into a flask Response object'''
    return Response( status = ReqResponse.status_code, \
            response = ReqResponse.content, \
            mimetype = ContentType )

