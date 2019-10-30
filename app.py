from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from models.querys import *

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app)

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    print(username, password)
    try:
        User.get(User.username == username, User.password == password)
    except:
        return False
    return True

@app.route("/", methods=['GET'])
@auth.login_required
def test():
    return jsonify("Hello, %s!" % auth.username())

@app.route("/task", methods=['GET'])
@auth.login_required
def tasks_list():
    offset = request.args.get("offset", default=0, type = int)
    limit = request.args.get("limit", default=15, type = int)
    return jsonify(get_task_list_query(offset, limit))

@app.route("/task/<int:task_id>", methods=['GET'])
@auth.login_required
def tasks(task_id):
    return jsonify(get_task_query(task_id))

@app.route("/task/create", methods=['POST'])
@auth.login_required
def create_task():
    task = request.get_json()
    create_task_query(task, auth.username())
    return jsonify("ok")

@app.route("/task/<int:task_id>/update", methods=['PUT'])
@auth.login_required
def update_task(task_id):
    task = request.get_json()
    update_task_query(task_id, task, auth.username())
    return jsonify("ok")

@app.route("/task/<int:task_id>/delete", methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = request.get_json()
    delete_task_query(task_id, auth.username())
    return jsonify("ok")

@app.route("/task/<int:task_id>/reset", methods=['get'])
@auth.login_required
def reset_task(task_id):
    return jsonify("ok")

@app.route("/task/<int:task_id>/run", methods=['get'])
@auth.login_required
def run_task(task_id):
    return jsonify("ok")

if __name__ == '__main__':
    app.run()