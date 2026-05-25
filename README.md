# Spam Message Detection

This project trains a machine learning model that predicts whether a message is spam or not spam.

It uses:

- A labelled dataset of spam and non-spam messages
- Basic text vectorization with word counts
- A Multinomial Naive Bayes classifier
- Model evaluation with accuracy
- A command-line predictor and a simple desktop app

## Project Structure

```text
spam/
  data/spam_messages.csv      Dataset used for training
  models/spam_model.json      Saved model after training
  src/spam_detector.py        Text processing and classifier code
  train_model.py              Trains and evaluates the model
  predict.py                  Command-line prediction program
  app.py                      Desktop GUI program
  web_app.py                  Webpage and backend API server
  web/                        HTML, CSS, and JavaScript files
```

## How To Run

Train the model:

```bash
python train_model.py
```

Predict from the command line:

```bash
python predict.py
```

Open the desktop app:

```bash
python app.py
```

Open the webpage:

```bash
python web_app.py
```

If `python` is not recognized on Windows, use:

```bash
py web_app.py
```

Then visit:

```text
http://127.0.0.1:8000
```

On Windows, you can also double-click:

```text
start_spam_checker.bat
```

Keep the terminal window open while using the site. If Chrome says
`127.0.0.1 refused to connect`, the local Python server is not running yet
or was closed. Start `web_app.py` again, wait for the message
`Spam detector web app running at http://127.0.0.1:8000`, then refresh the
browser.

If both `python web_app.py` and `py web_app.py` fail, install Python 3 from
the official Python website. During installation, select `Add python.exe to
PATH`, then open a new terminal and try again.

## Webpage Notes

The webpage sends the entered message text to the Python backend at `/api/predict`. The backend loads the trained model and returns the spam result with probability scores.

The upload button accepts message screenshots, but this computer does not currently have OCR installed. For accurate results, paste or type the message/email text into the text box.

## Example Messages

Spam example:

```text
Congratulations you have won a free prize click now
```

Not spam example:

```text
Can you send me the notes from class?
```

## Algorithm Summary

The program converts each message into lowercase word tokens. During training, it counts how often words appear in spam and non-spam messages. Naive Bayes then calculates which class is more likely for a new message. Laplace smoothing is used so unknown or rare words do not break the prediction.
