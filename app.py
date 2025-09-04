import os
import logging
from flask import Flask, render_template, request, jsonify
from controller import get_controller

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("app")

app = Flask(__name__, static_url_path="/static")
controller = get_controller()

STREAM_URL = os.environ.get("STREAM_URL", "http://127.0.0.1:81/stream")

@app.route("/")
def index():
    return render_template("index.html", stream_url=STREAM_URL)

@app.post("/api/move")
def move():
    direction = request.json.get("dir")
    try:
        getattr(controller, direction)()
        return jsonify(ok=True)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 400

@app.post("/api/stop")
def stop():
    controller.stop()
    return jsonify(ok=True)

@app.post("/api/fire")
def fire():
    controller.fire()
    return jsonify(ok=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

