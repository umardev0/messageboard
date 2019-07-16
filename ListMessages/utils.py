import redis
import json
from dicttoxml import dicttoxml
from flask import jsonify, abort, make_response

"""Redis connector."""
redisdb = redis.Redis(host='localhost', port=6379, decode_responses=True)

"""Resource variable with available resources. Used in error responses"""
resources = {'resources': [
            {'version-1': {
                'path': '/v1',
                'allowed-methods' : ['GET']}
            },
            {'version-2': {
                'default-format': 'JSON',
                'supported-formats': ['XML', 'JSON'],
                'path': '/v2?format=',
                'allowed-methods' : ['GET']}
            }
        ]}

def get_messages(version, format='JSON'):
    """
    Helper fucntion for GET method to obtain messages from data store.
    Parameters:
        version (string): Version to get messages for
        format (string): Format in which response is required. Default value JSON.
    """
    if version == 'v1':
        return __get_messages_v1()

    elif version == 'v2':
        return __get_messages_v2(format)
    # elif version == 'v3':
    #     return get_messages_v3()
    else:
        abort(400, 'Requested version not supported')

def __get_messages_v1():
    """
    Private fucntion to get messages for version 1.
    """
    messages = []
    for key in redisdb.scan_iter("msg:*"):
        message = json.loads(redisdb.get(key))
        message.pop('url', None)
        messages.append(message)
    return jsonify({'messages': messages}), 200

def __get_messages_v2(format):
    """
    Private fucntion to get messages for version 2.
    Parameters:
        format (string): Format in which response is required.
    """
    messages = []
    for key in redisdb.scan_iter("msg:*"):
        message = json.loads(redisdb.get(key))
        messages.append(message)

    if format.upper() == 'XML':
        def item_rename(x): return 'message'
        xml = dicttoxml(messages, custom_root='messages',
                        attr_type=False, item_func=item_rename)
        response = make_response(xml, 200)
        response.headers['Content-Type'] = 'application/xml'
        return response
    elif format.upper() == 'JSON':
        return jsonify({'messages': messages}), 200
    else:
        abort(400, 'Requested format not supported')

def __get_messages_v3():
    """
    API could be extended for new versions by simply adding new 
    methods for new versions.
    """
    return