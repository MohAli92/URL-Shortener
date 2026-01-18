from flask import Flask, jsonify, request, redirect, render_template

app = Flask(__name__)

counter = 1
url_store = {}

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok")

@app.route("/shorten", methods=["POST"])
def shorten_url():
    global counter

    data = request.get_json(silent=True) or request.form

    if not data or "url" not in data:
        return jsonify(error="URL is required"), 400

    original_url = data["url"].strip()

    
    if not original_url.startswith(("http://", "https://")):
        original_url = "https://" + original_url

    short_code = str(counter)
    url_store[short_code] = original_ur
    counter += 1

    short_url = f"/{short_code}"

    return jsonify(
        original_url=original_url,
        short_url=short_url
    )

@app.route("/<short_code>", methods=["GET"])
def redirect_to_original(short_code):
    if short_code not in url_store:
        return jsonify(error="Short URL not found"), 404

    return redirect(url_store[short_code])

if __name__ == "__main__":
    app.run(debug=True)
