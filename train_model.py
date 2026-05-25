from pathlib import Path
import random

from src.spam_detector import SpamDetector, load_dataset


DATA_PATH = Path("data/spam_messages.csv")
MODEL_PATH = Path("models/spam_model.json")


def accuracy_score(actual, predicted):
    correct = sum(1 for real, guess in zip(actual, predicted) if real == guess)
    return correct / len(actual)


def main():
    messages, labels = load_dataset(DATA_PATH)
    examples = list(zip(messages, labels))
    random.Random(42).shuffle(examples)
    split_index = int(len(examples) * 0.8)

    train_examples = examples[:split_index]
    test_examples = examples[split_index:]
    train_messages = [message for message, _ in train_examples]
    train_labels = [label for _, label in train_examples]
    test_messages = [message for message, _ in test_examples]
    test_labels = [label for _, label in test_examples]

    model = SpamDetector()
    model.fit(train_messages, train_labels)
    predictions = [model.predict(message) for message in test_messages]
    accuracy = accuracy_score(test_labels, predictions)
    model.save(MODEL_PATH)

    print(f"Training messages: {len(train_messages)}")
    print(f"Testing messages: {len(test_messages)}")
    print(f"Accuracy: {accuracy:.2%}")
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    main()
