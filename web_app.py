import cgi
import json
import shutil
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from src.spam_detector import SpamDetector


HOST = "127.0.0.1"
PORT = 8000
MODEL_PATH = Path("models/spam_model.json")
INDEX_PATH = Path("web/index.html")
STYLE_PATH = Path("web/styles.css")
SCRIPT_PATH = Path("web/script.js")


def ensure_model():
    if not MODEL_PATH.exists():
        subprocess.run([sys.executable, "train_model.py"], check=True)


def classify_message(model, message):
    prediction = model.predict(message)
    probabilities = model.predict_proba(message)
    spam_probability = probabilities.get("spam", 0) * 100
    not_spam_probability = probabilities.get("ham", 0) * 100
    confidence = max(spam_probability, not_spam_probability)

    return {
        "ok": True,
        "prediction": "SPAM" if prediction == "spam" else "NOT SPAM",
        "spamProbability": round(spam_probability, 2),
        "notSpamProbability": round(not_spam_probability, 2),
        "confidence": round(confidence, 2),
    }


def ocr_available():
    return shutil.which("tesseract") is not None


class SpamWebHandler(BaseHTTPRequestHandler):
    model = None

    def do_GET(self):
        route = urlparse(self.path).path
        if route == "/":
            self.send_file(INDEX_PATH, "text/html")
        elif route == "/styles.css":
            self.send_file(STYLE_PATH, "text/css")
        elif route == "/script.js":
            self.send_file(SCRIPT_PATH, "application/javascript")
        else:
            self.send_json({"ok": False, "error": "Page not found"}, status=404)

    def do_POST(self):
        if urlparse(self.path).path != "/api/predict":
            self.send_json({"ok": False, "error": "Endpoint not found"}, status=404)
            return

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE": self.headers.get("Content-Type"),
            },
        )

        message = form.getvalue("message", "").strip() if "message" in form else ""
        uploaded_file = form["screenshot"] if "screenshot" in form else None
        has_upload = bool(uploaded_file is not None and uploaded_file.filename)

        if message:
            result = classify_message(self.model, message)
            result["source"] = "typed text"
            self.send_json(result)
            return

        if has_upload:
            if not ocr_available():
                self.send_json(
                    {
                        "ok": False,
                        "needsText": True,
                        "error": (
                            "Screenshot uploaded, but OCR is not installed on this "
                            "computer. Please paste the message/email text in the "
                            "text box for an accurate result."
                        ),
                    },
                    status=422,
                )
                return

            self.send_json(
                {
                    "ok": False,
                    "needsText": True,
                    "error": "OCR support is not configured in this project yet.",
                },
                status=422,
            )
            return

        self.send_json(
            {"ok": False, "error": "Please enter a message or upload a screenshot."},
            status=400,
        )

    def send_file(self, path, content_type):
        if not path.exists():
            self.send_json({"ok": False, "error": f"Missing file: {path}"}, status=404)
            return

        content = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def send_json(self, data, status=200):
        content = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format, *args):
        print("%s - %s" % (self.address_string(), format % args))


def main():
    ensure_model()
    SpamWebHandler.model = SpamDetector.load(MODEL_PATH)
    server = ThreadingHTTPServer((HOST, PORT), SpamWebHandler)
    print(f"Spam detector web app running at http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop the server.")
    server.serve_forever()


if __name__ == "__main__":
    main()
