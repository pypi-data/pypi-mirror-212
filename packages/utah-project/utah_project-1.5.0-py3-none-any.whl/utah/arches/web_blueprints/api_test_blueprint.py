from flask import Flask, request
from flask_restful import Resource, Api
from flask import Blueprint
from utah.core.authorize import uri_authorized
from utah.core.authorize import UnauthorizedException


errors = {
    'UnauthorizedException': {
        'message': "User Not logged in",
        'status': 401
    },
    'ForbiddenException': {
        'message': "Authorization Error",
        'status': 403
    }
}


app = Blueprint('api_test01', __name__, url_prefix="/api_test")
api = Api(app, errors=errors, decorators=[uri_authorized()])

class HelloWorld(Resource):
    #method_decorators = {'get': [uri_authorized()]}

    def get(self, todo_id):
        return {'hello': 'world %s' % todo_id}

api.add_resource(HelloWorld, '/todo/<string:todo_id>')


@app.route("/gack", methods=["GET"])
def gack():
    return "gack"