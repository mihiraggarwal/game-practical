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
    node = convert_to_class(node)
    return main_spne(node)

@app.route("/nash", methods=["POST"])
def nash():
    node = request.json
    node = convert_to_class(node)
    return main_nash(node)

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