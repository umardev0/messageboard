from flask import Flask, jsonify, request, abort
from werkzeug.exceptions import HTTPException
import utils

app = Flask(__name__)

@app.route('/<string:version>', methods=['GET'])
def list_messages(version):
    if version.lower() == 'v1':
        if len(request.args.to_dict()) > 0:
            abort(400, 'This version does not accept additional parameters')

    return utils.get_messages(version, request.args.get('format', 'JSON'))

"""Custom global error handler with JSON response"""
@app.errorhandler(Exception)
def global_error_handler(error):
    code = 500
    if isinstance(error, HTTPException):
        code = error.code
    response = {'message': {'error' : error.description}}
    response.update(utils.resources)
    return jsonify(response), code

if __name__ == '__main__':
    app.run(host='localhost', port=7001)
