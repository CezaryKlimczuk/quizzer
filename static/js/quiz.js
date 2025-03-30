/********************************************************
 * Global Variables & Element References
 ********************************************************/
let quizSocket = null;
let currentQuestionId = null;
let timeLeft = 0;
let timerInterval = null;
let lastClickedButton = null;

const startQuizBtn = document.getElementById("startQuizBtn");
const quizContainer = document.getElementById("quizContainer");
const introContainer = document.getElementById("introContainer");
const participantCounter = document
  .getElementById("participantCounter")
  .querySelector("span");
const questionText = document.getElementById("questionText");
const answerButtons = document.getElementsByClassName("answer-btn");
const timerElement = document.getElementById("timer").querySelector("span");
const resultsContainer = document.getElementById("resultsContainer");
const finalMessage = document.getElementById("finalMessage");

/********************************************************
 * WebSocket Initialization & Event Handlers
 ********************************************************/
document.addEventListener("DOMContentLoaded", () => {
  // Retrieve the quiz ID from the "Start Quiz" button
  const quizId = startQuizBtn.dataset.quizId;

  // Use 'wss://' for production with HTTPS
  quizSocket = new WebSocket(`ws://${window.location.host}/ws/quiz/${quizId}/`);

  // Handle messages sent by the server
  quizSocket.onmessage = (e) => {
    const data = JSON.parse(e.data);
    console.log("Server says:", data);

    switch (data.action) {
      case "next_question":
        showQuestion(data);
        break;
      case "quiz_finished":
        showResults(data);
        break;
      case "user_count":
        participantCounter.textContent = data.active_users;
        break;
      case "answer_result":
        highlightUserAnswer(data.is_correct);
        break;
      default:
        console.warn("Unknown action:", data.action);
    }
  };

  quizSocket.onopen = () => {
    console.log("WebSocket connected.");
  };

  quizSocket.onclose = () => {
    console.log("WebSocket closed unexpectedly.");
  };
});

/********************************************************
 * DOM Event Listeners
 ********************************************************/
startQuizBtn.addEventListener("click", () => {
  // Notify server to start quiz, then show quiz container
  quizSocket.send(JSON.stringify({ action: "start_quiz" }));
  startQuizBtn.style.display = "none";
  quizContainer.style.display = "block";
  introContainer.style.display = "none";
});

// Attach click listener to each answer button
[...answerButtons].forEach((button) => {
  button.addEventListener("click", () => {
    lastClickedButton = button;

    // Disable all buttons to prevent multiple submissions
    [...answerButtons].forEach((b) => (b.disabled = true));

    // Send the user's choice to the server
    quizSocket.send(
      JSON.stringify({
        action: "submit_answer",
        question_id: currentQuestionId,
        answer_text: button.textContent,
      })
    );

    // Stop the timer once an answer is submitted
    stopTimer();
  });
});

/********************************************************
 * Core Quiz Functions
 ********************************************************/
function showQuestion(data) {
  // Reset button state before displaying the next question
  resetAnswerButtons();

  // Update question info
  currentQuestionId = data.question_id;
  questionText.textContent = data.question_text;
  timeLeft = data.time_limit;
  timerElement.textContent = timeLeft;

  // Populate answer button text
  const answers = data.question_answers || [];
  [...answerButtons].forEach((btn, idx) => {
    btn.textContent = answers[idx] || "";
  });

  // Start the countdown for this question
  startTimer();
}

function showResults(data) {
  // Hide quiz elements and show the final score message
  quizContainer.style.display = "none";
  resultsContainer.style.display = "block";
  finalMessage.textContent = `${data.message} Score: ${data.score}`;
}

/********************************************************
 * User Feedback Utilities
 ********************************************************/
function highlightUserAnswer(isCorrect) {
  if (!lastClickedButton) return;
  lastClickedButton.style.backgroundColor = isCorrect ? "green" : "red";
}

function resetAnswerButtons() {
  [...answerButtons].forEach((button) => {
    button.style.backgroundColor = "";
    button.disabled = false;
  });
}

/********************************************************
 * Timer Utilities
 ********************************************************/
function startTimer() {
  // Clear any existing timer before starting a new one
  stopTimer();
  timerInterval = setInterval(() => {
    timeLeft--;
    timerElement.textContent = timeLeft;

    // If time runs out, automatically submit an empty answer
    if (timeLeft <= 0) {
      stopTimer();
      quizSocket.send(
        JSON.stringify({
          action: "submit_answer",
          question_id: currentQuestionId,
          answer_text: "", // or some fallback
        })
      );
    }
  }, 1000);
}

function stopTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}
