import logging

from flask import jsonify, Blueprint, Flask
from flask_cors import CORS
from utils import require_authorization, check_request_json


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("backend_functions")

functions = Blueprint("functions", "gpt_backend_functions", static_folder="./static_files")
CORS(functions)


@functions.route("/weather", methods=["POST"])
@require_authorization
def get_weather():
    data = check_request_json("address")
    address = data["address"]
    return jsonify({
        "今日天气": "晴",
        "地址": address
    }), 200


# Functions for GPT Plugins
@functions.route("/logo.png", methods=["GET"])
def get_logo():
    return functions.send_static_file("logo.png")


@functions.route("/.well-known/ai-plugin.json", methods=["GET"])
def get_manifest():
    """
    Get the manifest file that is required by GPT-Plugins
    :return:
    """
    return functions.send_static_file("manifest.json")


@functions.route("/openapi.yaml", methods=["GET"])
def get_openapi_spec():
    return functions.send_static_file("openapi.yaml")


@functions.route("/legal", methods=["GET"])
def get_legal_info():
    return "Legal", 200


# Functions for GPT Plugins End


if __name__ == "__main__":
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"
    app.register_blueprint(functions)
    app.run(host="0.0.0.0", debug=False, port=11111)
