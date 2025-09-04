import os
import usb.core 
import logging
from flask import Flask, render_template, request, jsonify

from playsound import play_wav

# Inspired by:
# https://github.com/pwicks86/usb_missile_control/blob/master/usb_missile_control/missile_control.py


logging.basicConfig(level=logging.INFO)
log = logging.getLogger("app")

app = Flask(__name__, static_url_path="/static")

STREAM_URL = "http://131.220.157.234:80/stream"

rocket = usb.core.find(idVendor=0x2123, idProduct=0x1010)
if rocket is None:
    log.error('Launcher not found.')
if rocket.is_kernel_driver_active(0) is True:
    rocket.detach_kernel_driver(0)
    rocket.set_configuration()

@app.route("/")
def index():
    return render_template("index.html", stream_url=STREAM_URL)

@app.post("/api/move")
def move():
    direction = request.json.get("dir")
    try:
        log.info(direction)
        match direction:
            case "up":
                rocket.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
            case "down":
                rocket.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
            case "left":
                rocket.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) 
            case "right":
                rocket.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
            case _:
                log.error("Can not parse direction")
        return jsonify(ok=True)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 400

@app.post("/api/stop")
def stop():
    log.info("stop")
    rocket.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    return jsonify(ok=True)

@app.post("/api/fire")
def fire():
    log.info("fire")
    rocket.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    return jsonify(ok=True)

@app.post("/api/sound")
def sound():
    name = request.json.get("name")
    try:
        log.info(name)
        match name:
            case "fatality":
                play_wav("static/sounds/fatality.wav")
            case "fire-in-the-hole":
                play_wav("static/sounds/fire-in-the-hole.wav")
            case "flashbang":
                play_wav("ststic/sounds/flashbang.wav")
            case "headshot":
                play_wav("static/sounds/headshot.wav")
            case "monster-kill":
                play_wav("static/sounds/monster-kill.wav")
            case _:
                log.error("Can not parse sound name")
        return jsonify(ok=True)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

