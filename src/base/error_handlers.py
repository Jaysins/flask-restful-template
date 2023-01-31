from src import app
from flask import jsonify


@app.errorhandler(404)
def custom404(data):
    response = jsonify(data)
    response.status_code = 404
    response.status = "error.NotFound"
    return response


@app.errorhandler(401)
def custom401(data):
    response = jsonify(data)
    response.status_code = 401
    response.status = "error.Unauthorized"
    return response


@app.errorhandler(409)
def custom409(data):
    response = jsonify(data)
    response.status_code = 409
    response.status = "error.Validation Failed"
    return response
