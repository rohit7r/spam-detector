from pathlib import Path
import subprocess
import sys
import tkinter as tk
from tkinter import ttk

from src.spam_detector import SpamDetector


MODEL_PATH = Path("models/spam_model.json")


def ensure_model():
    if not MODEL_PATH.exists():
        subprocess.run([sys.executable, "train_model.py"], check=True)


class SpamApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Spam Message Detection")
        self.geometry("720x460")
        self.minsize(640, 420)
        self.configure(bg="#f6f8fb")

        ensure_model()
        self.model = SpamDetector.load(MODEL_PATH)

        self.message_var = tk.StringVar()
        self.result_var = tk.StringVar(value="Enter a message to check whether it is spam.")
        self.confidence_var = tk.StringVar(value="")

        self.create_widgets()

    def create_widgets(self):
        container = ttk.Frame(self, padding=24)
        container.pack(fill="both", expand=True)

        title = ttk.Label(
            container,
            text="Spam Message Detection",
            font=("Segoe UI", 22, "bold"),
        )
        title.pack(anchor="w")

        subtitle = ttk.Label(
            container,
            text="A simple machine learning classifier using text vectorization and Naive Bayes.",
            font=("Segoe UI", 11),
        )
        subtitle.pack(anchor="w", pady=(4, 20))

        label = ttk.Label(container, text="Message", font=("Segoe UI", 11, "bold"))
        label.pack(anchor="w")

        self.message_box = tk.Text(
            container,
            height=7,
            wrap="word",
            font=("Segoe UI", 12),
            relief="solid",
            bd=1,
        )
        self.message_box.pack(fill="x", pady=(6, 14))

        button = ttk.Button(container, text="Predict", command=self.predict_message)
        button.pack(anchor="w")

        result_frame = ttk.Frame(container, padding=(0, 20, 0, 0))
        result_frame.pack(fill="x")

        self.result_label = ttk.Label(
            result_frame,
            textvariable=self.result_var,
            font=("Segoe UI", 16, "bold"),
        )
        self.result_label.pack(anchor="w")

        confidence = ttk.Label(
            result_frame,
            textvariable=self.confidence_var,
            font=("Segoe UI", 11),
        )
        confidence.pack(anchor="w", pady=(6, 0))

    def predict_message(self):
        message = self.message_box.get("1.0", "end").strip()
        if not message:
            self.result_var.set("Please enter a message first.")
            self.confidence_var.set("")
            return

        prediction = self.model.predict(message)
        probabilities = self.model.predict_proba(message)
        spam_percent = probabilities.get("spam", 0) * 100
        ham_percent = probabilities.get("ham", 0) * 100

        if prediction == "spam":
            self.result_var.set("Prediction: SPAM")
        else:
            self.result_var.set("Prediction: NOT SPAM")

        self.confidence_var.set(
            f"Spam: {spam_percent:.2f}%   |   Not spam: {ham_percent:.2f}%"
        )


if __name__ == "__main__":
    app = SpamApp()
    app.mainloop()
