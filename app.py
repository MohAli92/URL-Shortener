from flask import Flask, jsonify, request, redirect, render_template
from datetime import datetime, timedelta
from time import time
from urllib.parse import urlparse

app = Flask(__name__)

app.config["TESTING"] = False

# ================= CONFIG =================
USERNAME = "nouh"
DEFAULT_EXPIRATION_HOURS = 1
RATE_LIMIT_SECONDS = 2
# =========================================

# short_code -> { url, expires_at }
url_store = {}

# original_url -> short_code
reverse_store = {}

# ip -> last_request_time
rate_limit = {}


@app.route("/")
def home():
    return 


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/shorten", methods=["POST"])
def shorten_url():
    ip = request.remote_addr
    now = time()

    # ---------- Rate limiting ----------
    if not app.config.get("TESTING"):
        last_time = rate_limit.get(ip, 0)
        if now - last_time < RATE_LIMIT_SECONDS:
            return jsonify(error="Too many requests"), 429
        rate_limit[ip] = now
    # -----------------------------------

    data = request.get_json(silent=True) or request.form
    if not data or "url" not in data:
        return jsonify(error="URL is required"), 400

    original_url = data["url"].strip()

    if not original_url.startswith(("http://", "https://")):
        original_url = "https://" + original_url

    alias = data.get("alias")

    # ---------- Deduplication ----------
    if original_url in reverse_store:
        short_code = reverse_store[original_url]
    else:
        if alias:
            if alias in url_store:
                return jsonify(error="Alias already in use"), 409
            short_code = alias
        else:
            parsed = urlparse(original_url)
            domain = parsed.netloc.lower()

            if domain.startswith("www."):
                domain = domain.replace("www.", "")

            base_name = domain.split(".")[0]
            short_code = base_name

            i = 2
            while short_code in url_store:
                short_code = f"{base_name}{i}"
                i += 1

        expires_at = datetime.now() + timedelta(hours=DEFAULT_EXPIRATION_HOURS)

        url_store[short_code] = {
            "url": original_url,
            "expires_at": expires_at
        }
        reverse_store[original_url] = short_code
    # -----------------------------------

    return jsonify(
        original_url=original_url,
        short_url=f"/{USERNAME}/{short_code}",
        preview_url=f"/{USERNAME}/preview/{short_code}"
    )


@app.route(f"/{USERNAME}/<short_code>")
def redirect_to_original(short_code):
    data = url_store.get(short_code)

    if not data:
        return jsonify(error="Short URL not found"), 404

    if datetime.now() > data["expires_at"]:
        return jsonify(error="This link has expired"), 410

    return redirect(data["url"])


@app.route(f"/{USERNAME}/preview/<short_code>")
def preview(short_code):
    data = url_store.get(short_code)
    if not data:
        return "Not found", 404

    return render_template("preview.html", url=data["url"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
