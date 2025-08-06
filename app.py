from flask import Flask, render_template, redirect, url_for
from gofile import upload_to_gofile

app = Flask(__name__)
LOG_FILE = "logs/events.log"
last_upload_link = None

@app.route("/")
def index():
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()[-10:]
    except:
        lines = ["Log file not found."]
    return render_template("index.html", logs=lines, download_link=last_upload_link)

@app.route("/upload")
def upload():
    global last_upload_link
    last_upload_link = upload_to_gofile(LOG_FILE)
    print("🔗 Uploaded link:", last_upload_link)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
