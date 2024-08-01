import os
import dotenv
from flask import Flask, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from api.solver import main_spne, main_nash, Node

dotenv.load_dotenv()

CLIENT_URL = os.environ.get('CLIENT_URL')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": [CLIENT_URL]}})

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)

@app.route("/")
def index():
    return "game-practical"

@app.route("/spne", methods=["POST"])
def spne():
    node = request.json
    if not validate_tree(node):
        return {"error": "Invalid tree"}
    node = convert_to_class(node)

    try:
        n = main_spne(node)
        return n
    except Exception as e:
        print(e)
        return {"error": "Something went wrong"}

@app.route("/nash", methods=["POST"])
def nash():
    node = request.json
    if not validate_tree(node):
        return {"error": "Invalid tree"}
    node = convert_to_class(node)

    try:
        n = main_nash(node)
        return n
    except Exception as e:
        print(e)
        return {"error": "Something went wrong"}

def convert_to_class(node):
    n0 = Node(
        node_number=node["node_number"],
        player=node["player"] - 1,
        children=list(map(lambda x: [x], node["children"])),
        actions=node["actions"],
        imperfect_to=node["imperfect_to"],
        payoffs=node["payoffs"]
    )
    for i in range(len(n0.children)):
        n = convert_to_class(n0.children[i][0])
        n0.children[i][0] = n
    return n0

def validate_tree(node):
    if node["player"] < 0:
        return False
    if len(node["payoffs"]) == 0 and len(node["children"]) == 0:
        return False
    if len(node["children"]) != len(node["actions"]):
        return False
    
    for i in range(len(node["children"])):
        if len(node["children"][i]["imperfect_to"]) > 0:
            if len(node["children"][i]["payoffs"]) > 0:
                return False
            for j in range(len(node["children"][i]["imperfect_to"])):
                if node["children"][i]["imperfect_to"][j] not in [k["node_number"] for k in node["children"]]:
                    return False
        if not validate_tree(node["children"][i]):
            return False
        
    return True