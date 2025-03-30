let quizSocket = null;
let currentQuestionId = null;
let timeLeft = 0;
let timerInterval = null;

const startQuizBtn = document.getElementById("startQuizBtn");
const quizContainer = document.getElementById("quizContainer");
const introContainer = document.getElementById("introContainer");
const participantCounter = document.getElementById("participantCounter").querySelector("span");
const questionText = document.getElementById("questionText");
const answerButtons = document.getElementsByClassName("answer-btn");
const timerElement = document.getElementById("timer").querySelector("span");
const resultsContainer = document.getElementById("resultsContainer");
const finalMessage = document.getElementById("finalMessage");

let correctAnswer = null;

// On page load, create the WebSocket connection
document.addEventListener("DOMContentLoaded", () => {
  const startQuizBtn = document.getElementById("startQuizBtn");
  const quizId = startQuizBtn.dataset.quizId;
  // For production with HTTPS, use wss://
  quizSocket = new WebSocket(`ws://${window.location.host}/ws/quiz/${quizId}/`);

  quizSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log("Server says:", data);
    if (data.action === "next_question") {
      showQuestion(data);
    } else if (data.action === "quiz_finished") {
      showResults(data);
    } else if (data.action === "user_count") {
      participantCounter.textContent = data.active_users;
    }
  };

  quizSocket.onopen = function(e) {
    console.log("WebSocket connected.");
  };

  quizSocket.onclose = function(e) {
    console.log("WebSocket closed unexpectedly.");
  };
});

startQuizBtn.addEventListener("click", () => {
  // Start the quiz by sending an action
  quizSocket.send(JSON.stringify({ action: "start_quiz" }));
  startQuizBtn.style.display = "none";
  quizContainer.style.display = "block";
  introContainer.style.display = "none";
});

[...answerButtons].forEach((button) => {
  console.log("Adding click listeners now.")
  button.addEventListener("click", () => {
    // Prevent any further clicks
    [...answerButtons].forEach(b => b.disabled = true);

    // Always highlight the correct button in green
    const correctBtn = [...answerButtons].find(btn => btn.textContent === correctAnswer);
    if (correctBtn) {
      correctBtn.style.backgroundColor = "green";
    }

    // If user clicked the wrong button, highlight it red
    if (button.textContent !== correctAnswer) {
      button.style.backgroundColor = "red";
    }

    // Wait 1.5s before sending the answer via WebSocket
    setTimeout(() => {
      quizSocket.send(JSON.stringify({
        action: "submit_answer",
        question_id: currentQuestionId,
        answer_text: button.textContent
      }));
      stopTimer();
    }, 1500);
  });
});

function resetAnswerButtons() {
  [...answerButtons].forEach((button) => {
    button.style.backgroundColor = "";
    button.disabled = false;
  });
}


function showQuestion(data) {
  resetAnswerButtons();
  currentQuestionId = data.question_id;
  correctAnswer = data.correct_answer;
  questionText.textContent = data.question_text;
  timeLeft = data.time_limit;
  timerElement.textContent = timeLeft;

  console.log('Hello!!');

  console.log(data.question_answers);

  for (let i = 0; i < [...answerButtons].length; i++) {
    [...answerButtons][i].textContent = data.question_answers[i] || "";
  }

  startTimer();
}

function startTimer() {
  stopTimer(); // clear any existing interval
  timerInterval = setInterval(() => {
    timeLeft--;
    timerElement.textContent = timeLeft;
    if (timeLeft <= 0) {
      stopTimer();
      // Automatically submit empty or partial answer if time runs out
      quizSocket.send(JSON.stringify({
        action: "submit_answer",
        question_id: currentQuestionId,
        answer_text: answerInput.value
      }));
      answerInput.value = "";
    }
  }, 1000);
}

function stopTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

function showResults(data) {
  quizContainer.style.display = "none";
  resultsContainer.style.display = "block";
  finalMessage.textContent = data.message + " Score: " + data.score;
}