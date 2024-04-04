from flask import Flask, Response
import requests
import time
import os

app = Flask(__name__)

camera_url = os.environ["CAMERA_URL"]
port = int(os.environ.get("PORT", "3000"))
delay = float(os.environ.get("DELAY", "0.1"))


def fetch_frame():
    try:
        r = requests.get(camera_url, stream=True)
        if r.status_code == 200:
            return r.content
    except Exception as e:
        print("Error fetching frame:", e)
    return None


def generate_mjpeg():
    while True:
        frame = fetch_frame()
        if frame:
            yield (
                b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"
            )
        time.sleep(delay)  # Adjust the delay as needed


@app.route("/mjpeg_stream")
def mjpeg_stream():
    return Response(
        generate_mjpeg(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=True)
