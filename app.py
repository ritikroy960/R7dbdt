
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/watch/<video_id>")
def watch(video_id):
    embed_url = f"https://streamtape.com/e/{video_id}/"
    return render_template("watch.html", embed_url=embed_url)

@app.route("/")
def home():
    return "✅ Streamtape Watch Page is Live!"

if __name__ == "__main__":
    app.run()
