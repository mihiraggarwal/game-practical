from flask import Flask, request
from flask_cors import CORS

from api.solver import main_spne, main_nash, Node

app = Flask(__name__)
CORS(app)

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