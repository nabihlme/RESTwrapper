
# old required keys for json payload
requiredKeys = ['internalMetadata', 'minidMetadata']
requiredInternalMetadata = ['_target', '_profile', '_status', '_export', '_crossref'] 
requiredMinidMetadata = ['identifier', 'created', 'checksum', 'checksumMethod', 'status', 'locations', 'titles']

# old helper functions for determining the type of object
def DataCatalogue(PassedDict):
    if set(PassedDict.keys()) == set(['@context', '@id', '@type', 'identifier', 'name']): 
        return True
    else:
        return False

def DatasetUnpublished(PassedDict):
    if set(PassedDict.keys()) == set(['@context', '@id', '@type', 'identifier', 'includedInDataCatalogue', 'dateCreated', 'distrobution']): 
        return True
    else:
        return False

def DatasetPublished(PassedDict):
    if  set(PassedDict.keys()) == set(['@context', '@id', '@type', 'identifier', 'includedInDataCatalougue', \
            'dateCreated', 'datePublished', 'distribution', 'author', 'name', 'descripition', 'keywords', \
            'version', 'citation']): 
        return True
    else:
        return False

def DatasetDownload(PassedDict):
    if set(PassedDict.keys()) ==  set(['@context', '@id', '@type', 'identifier', 'version', 'contentSize']): 
        return True
    else:
        return False
