from pathlib import Path

from src.spam_detector import SpamDetector


MODEL_PATH = Path("models/spam_model.json")


def main():
    if not MODEL_PATH.exists():
        raise SystemExit("Model not found. Run: python train_model.py")

    model = SpamDetector.load(MODEL_PATH)
    print("Spam Message Detection")
    print("Type a message and press Enter. Type 'exit' to stop.")

    while True:
        message = input("\nMessage: ").strip()
        if message.lower() in {"exit", "quit"}:
            break
        if not message:
            print("Please enter a message.")
            continue

        prediction = model.predict(message)
        probabilities = model.predict_proba(message)
        spam_percent = probabilities.get("spam", 0) * 100
        ham_percent = probabilities.get("ham", 0) * 100

        display_prediction = "SPAM" if prediction == "spam" else "NOT SPAM"
        print(f"Prediction: {display_prediction}")
        print(f"Spam probability: {spam_percent:.2f}%")
        print(f"Not spam probability: {ham_percent:.2f}%")


if __name__ == "__main__":
    main()
