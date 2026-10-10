/* EduGenie - frontend logic (vanilla JS, no build step).
 * All AI-generated text is inserted with textContent (never innerHTML) so it cannot inject markup. */
"use strict";

const ENDPOINTS = {
  explain: "/explain",
  qa: "/qa",
  quiz: "/quiz",
  summarize: "/summarize",
  recommend: "/learn/recommendations",
};
const LETTERS = ["A", "B", "C", "D"];

const form = document.getElementById("edugenie-form");
const taskSelect = document.getElementById("task");
const inputBox = document.getElementById("user-input");
const followupRow = document.getElementById("followup-row");
const followupBox = document.getElementById("followup");
const submitBtn = document.getElementById("submit-btn");
const statusBox = document.getElementById("status");
const resultBox = document.getElementById("result");

// The previous question and answer, kept in memory only, used for follow-up questions.
let lastQuestion = "";
let lastAnswer = "";

// The follow-up option is only shown for "Ask a question" once an answer exists.
taskSelect.addEventListener("change", () => {
  followupRow.hidden = taskSelect.value !== "qa" || !lastAnswer;
});

function showError(message) {
  statusBox.textContent = message;
  statusBox.className = "status error";
  resultBox.hidden = true;
}

function showText(text) {
  resultBox.className = "result";
  resultBox.textContent = text;
  resultBox.hidden = false;
}

function showQuiz(questions) {
  resultBox.className = "result";
  resultBox.textContent = "";
  questions.forEach((q, qi) => {
    const card = document.createElement("div");
    card.className = "quiz-card";

    const title = document.createElement("p");
    title.className = "quiz-question";
    title.textContent = `${qi + 1}. ${q.question}`;
    card.appendChild(title);

    const feedback = document.createElement("p");
    feedback.className = "quiz-feedback";

    q.options.forEach((option, oi) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "quiz-option";
      btn.textContent = `${LETTERS[oi]}. ${option}`;
      btn.addEventListener("click", () => {
        const buttons = card.querySelectorAll(".quiz-option");
        buttons.forEach((b) => (b.disabled = true));
        if (oi === q.answer_index) {
          btn.classList.add("correct");
          feedback.textContent = "Correct!";
        } else {
          btn.classList.add("wrong");
          buttons[q.answer_index].classList.add("correct");
          feedback.textContent = `Not quite. The correct answer is ${LETTERS[q.answer_index]}. ${q.options[q.answer_index]}`;
        }
      });
      card.appendChild(btn);
    });

    card.appendChild(feedback);
    resultBox.appendChild(card);
  });
  resultBox.hidden = false;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const task = taskSelect.value;
  const text = inputBox.value.trim();

  if (!text) {
    showError("Please enter a question or topic first.");
    return;
  }

  const payload = { text: text, context: "" };
  if (task === "qa" && followupBox.checked && lastAnswer) {
    payload.context = `Student asked: ${lastQuestion}\nEduGenie answered: ${lastAnswer}`;
  }

  submitBtn.disabled = true;
  statusBox.textContent = "EduGenie is thinking...";
  statusBox.className = "status";
  resultBox.hidden = true;

  try {
    const response = await fetch(ENDPOINTS[task], {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      showError(data.detail || "Something went wrong. Please try again.");
      return;
    }

    statusBox.textContent = "";
    if (task === "quiz") {
      showQuiz(data.questions);
    } else {
      showText(data.result);
    }

    if (task === "qa") {
      lastQuestion = text;
      lastAnswer = data.result;
      followupRow.hidden = false;
      followupBox.checked = false;
    }
  } catch (error) {
    showError("Could not reach the EduGenie server. Is it running?");
  } finally {
    submitBtn.disabled = false;
  }
});
