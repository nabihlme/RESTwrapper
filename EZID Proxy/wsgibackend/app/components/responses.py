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
            response = '{"You need to submit a request body"}',
            mimetype = 'application/ld+json'
        )

BadRequestBody = Response(
            status = 400,
            response = '{"Submitted Request Body was missing required parameters"}',
            mimetype = 'application/ld+json'
        )

BadANVL = Response(
            status = 400,
            response = '{"ANVL stored in EZID does not conform to current core metadata standards"}',
            mimetype = 'application/ld+json'
        )

MethodNotAllowed = Response(
            status = 405,
            response = '{"Method Not Supported, either PUT or GET"}',
            mimetype = 'application/ld+json'
        )

UnfinishedBuisness = Response(
        status = 501,
        response = '{"Not Yet Built, Working On It!"}',
        mimetype = 'application/ld+json'
        )


def InvalidParent(ID):
    message = 'No record of GUID {}'.format(ID)
    return Response( status = 404,\
            response = message, \
            mimetype = 'application/ld+json')

def buildResponse(ReqResponse, ContentType='application/ld+json'):
    '''Transfer requests response object into a flask Response object'''
    return Response( status = ReqResponse.status_code, \
            response = ReqResponse.content, \
            mimetype = ContentType )

