# Spam Message Detection Project Report

## Objective

The goal of this project is to build a machine learning system that can identify whether a text message is spam or not spam.

## Dataset

The dataset is stored in `data/spam_messages.csv`. It contains two columns:

- `label`: The category of the message, either `spam` or `ham`
- `message`: The text message

`ham` means the message is not spam.

## Method

The project uses basic text processing and a classification algorithm.

1. The message is converted to lowercase.
2. The message is split into word tokens.
3. The model counts how often each word appears in spam and non-spam messages.
4. A Multinomial Naive Bayes classifier calculates which class is more likely for a new message.

## Model

The model is implemented in `src/spam_detector.py`.

Naive Bayes is a good choice for this task because it is simple, fast, and commonly used for text classification problems such as spam detection.

## Training And Evaluation

The training script is `train_model.py`.

It performs these steps:

1. Loads the dataset.
2. Shuffles the examples.
3. Uses 80% of the data for training.
4. Uses 20% of the data for testing.
5. Prints the accuracy.
6. Saves the trained model to `models/spam_model.json`.

In the current run, the model achieved 90% accuracy on the test data.

## User Prediction System

The project includes two ways for a user to enter a message:

- `predict.py`: command-line prediction
- `app.py`: desktop app with a text box and predict button
- `web_app.py`: browser page with a backend prediction API

The webpage lets the user enter message or email text and then sends it to the backend for prediction. A screenshot upload control is also included, but screenshot text extraction requires OCR software such as Tesseract.

## Conclusion

This project demonstrates the basics of machine learning, text vectorization, model training, model evaluation, and prediction on new user input.
