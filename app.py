from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from queries.repository import *
from queries.user import *
from queries.task import *
import repository.scripts as scripts

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

#####################################
##  Task
#####################################
@app.route("/repository/check", methods=['POST'])
@auth.login_required
def check_repository():
    name = request.get_json()
    return jsonify(check_repository_query(name["name"]))


@app.route("/repository", methods=['GET'])
@auth.login_required
def get_repository_list():
    offset = request.args.get("offset", default=0, type = int)
    limit = request.args.get("limit", default=15, type = int)
    return jsonify(get_repository_list_query(offset, limit))

@app.route("/repository/my", methods=['GET'])
@auth.login_required
def get_my_repository_list():
    offset = request.args.get("offset", default=0, type = int)
    limit = request.args.get("limit", default=15, type = int)
    return jsonify(get_repository_list_query(offset, limit, auth.username()))

@app.route("/repository/count", methods=['GET'])
@auth.login_required
def get_repository_count():
    return jsonify(get_repository_count_query())

@app.route("/repository/my/count", methods=['GET'])
@auth.login_required
def get_my_repository_count():
    return jsonify(get_repository_count_query(auth.username()))

@app.route("/repository/<int:repository_id>", methods=['GET'])
@auth.login_required
def get_repository(repository_id):
    return jsonify(get_repository_query(repository_id))

@app.route("/repository/create", methods=['POST'])
@auth.login_required
def create_repository():
    task = request.get_json()
    create_repository_query(task, auth.username())
    return jsonify("ok")

@app.route("/repository/<int:repository_id>/update", methods=['PUT'])
@auth.login_required
def update_repository(repository_id):
    repository = request.get_json()
    update_repository_query(repository_id, repository, auth.username())
    return jsonify("ok")

@app.route("/repository/<int:repository_id>/delete", methods=['DELETE'])
@auth.login_required
def delete_repository(repository_id):
    delete_repository_query(repository_id, auth.username())
    return jsonify("ok")

@app.route("/repository/<int:repository_id>/reset", methods=['get'])
@auth.login_required
def reset_repository(repository_id):
    reset_repository_query(repository_id, auth.username())
    return jsonify("ok")

@app.route("/repository/<int:repository_id>/run", methods=['get'])
@auth.login_required
def run_task(repository_id):
    run_repository_query(repository_id, auth.username())
    return jsonify("ok")

#####################################
##  User
#####################################

@app.route("/user/check", methods=['POST'])
@auth.login_required
def check_user():
    name = request.get_json()
    return jsonify(check_user_query(name["name"]))

@app.route("/user/count", methods=['GET'])
@auth.login_required
def get_user_count():
    return jsonify(get_user_count_query())

@app.route("/user", methods=['GET'])
@auth.login_required
def get_user_list():
    offset = request.args.get("offset", default=0, type = int)
    limit = request.args.get("limit", default=15, type = int)
    return jsonify(get_user_list_query(offset, limit))

@app.route("/user/<int:user_id>", methods=['GET'])
@auth.login_required
def get_user(user_id):
    return jsonify(get_user_query(user_id))

@app.route("/user/create", methods=['POST'])
@auth.login_required
def create_user():
    user = request.get_json()
    print(user["username"])
    create_user_query(user, auth.username())
    return jsonify("ok")

@app.route("/user/<int:user_id>/update", methods=['PUT'])
@auth.login_required
def update_user(user_id):
    user = request.get_json()
    update_user_query(user_id, user, auth.username())
    return jsonify("ok")

@app.route("/user/<int:user_id>/delete", methods=['DELETE'])
@auth.login_required
def delete_user(user_id):
    delete_user_query(user_id, auth.username())
    return jsonify("ok")

@app.route("/user/check_group", methods=['GET'])
@auth.login_required
def get_group():
    return jsonify(get_group_query(auth.username()))


#####################################
##  Log
#####################################

@app.route("/task/count", methods=['GET'])
@auth.login_required
def get_task_count():
    return jsonify(get_task_count_query())

@app.route("/task", methods=['GET'])
@auth.login_required
def get_task_list():
    offset = request.args.get("offset", default=0, type = int)
    limit = request.args.get("limit", default=50, type = int)
    return jsonify(get_task_list_query(offset, limit))

@app.route("/task/<int:task_id>", methods=['GET'])
@auth.login_required
def get_task(task_id):
    return jsonify(get_task_query(task_id))

#####################################
##  zpool
#####################################

@app.route("/zpool", methods=['GET'])
@auth.login_required
def get_zpool_list_resp():
    #res = scripts.get_zpool_list()[1].decode('utf-8').split('\n')[:-1]
    return jsonify(["zroot"])

#####################################
##  Main
#####################################

if __name__ == '__main__':
    app.run()