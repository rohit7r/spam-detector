const form = document.querySelector("#predict-form");
const screenshotInput = document.querySelector("#screenshot");
const fileName = document.querySelector("#file-name");
const button = document.querySelector("#predict-button");
const clearButton = document.querySelector("#clear-button");
const messageInput = document.querySelector("#message");
const charCount = document.querySelector("#char-count");
const resultPanel = document.querySelector("#result");
const resultTitle = document.querySelector("#result-title");
const resultDetail = document.querySelector("#result-detail");
const statusIcon = document.querySelector("#status-icon");
const spamBar = document.querySelector("#spam-bar");
const spamScore = document.querySelector("#spam-score");
const hamScore = document.querySelector("#ham-score");

messageInput.addEventListener("input", updateCharCount);

screenshotInput.addEventListener("change", () => {
  const file = screenshotInput.files[0];
  fileName.textContent = file ? file.name : "OCR is optional. Text gives the best result.";
});

clearButton.addEventListener("click", () => {
  form.reset();
  fileName.textContent = "OCR is optional. Text gives the best result.";
  updateCharCount();
  setResult("idle", "Ready to check", "Paste a message and press Check. Keep the Python server window open while using this page.", null, null);
  messageInput.focus();
});

document.querySelectorAll(".sample-button").forEach((sampleButton) => {
  sampleButton.addEventListener("click", () => {
    messageInput.value = sampleButton.dataset.message;
    updateCharCount();
    messageInput.focus();
  });
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  button.disabled = true;
  clearButton.disabled = true;
  button.textContent = "Checking...";
  setResult("idle", "Checking...", "The backend model is running the prediction.", null, null);

  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      body: new FormData(form),
    });
    const data = await response.json();

    if (!response.ok || !data.ok) {
      setResult("error", "Need text input", data.error || "Unable to classify this input.", null, null);
      return;
    }

    const isSpam = data.prediction === "SPAM";
    const statusClass = isSpam ? "spam" : "safe";
    const title = isSpam ? "SPAM detected" : "NOT SPAM";
    const detail = `Confidence: ${data.confidence}% based on ${data.source}.`;
    setResult(statusClass, title, detail, data.spamProbability, data.notSpamProbability);
  } catch (error) {
    setResult("error", "Server error", "Please make sure the web server is still running.", null, null);
  } finally {
    button.disabled = false;
    clearButton.disabled = false;
    button.textContent = "Check";
  }
});

function setResult(type, title, detail, spam, ham) {
  resultPanel.className = `result-panel ${type}`;
  resultTitle.textContent = title;
  resultDetail.textContent = detail;
  statusIcon.textContent = getStatusIcon(type);
  const meterValue = Number.isFinite(spam) ? spam : 0;
  spamBar.style.width = `${meterValue}%`;
  spamScore.textContent = Number.isFinite(spam) ? `${spam}%` : "--";
  hamScore.textContent = Number.isFinite(ham) ? `${ham}%` : "--";
}

function updateCharCount() {
  const count = messageInput.value.length;
  charCount.textContent = `${count} ${count === 1 ? "character" : "characters"}`;
}

function getStatusIcon(type) {
  if (type === "spam") {
    return "!";
  }

  if (type === "safe") {
    return "OK";
  }

  if (type === "error") {
    return "i";
  }

  return "?";
}
