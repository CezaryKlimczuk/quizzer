document.addEventListener("DOMContentLoaded", () => {
  const quizCountSpans = {};
  const relevantQuizIds = [];

  // Gather your span elements (like before)
  document.querySelectorAll('[id^="quizUserCounterId"]').forEach((span) => {
    const quizId = span.id.replace('quizUserCounterId', '');
    quizCountSpans[quizId] = span;
    relevantQuizIds.push(quizId);

  });

  // For production with HTTPS, use wss://
  const globalNotificationSocket = new WebSocket(`ws://${window.location.host}/ws/global_notifications/`);

  globalNotificationSocket.onopen = function(e) {
    globalNotificationSocket.send(JSON.stringify({
      "action": "request_initial_counts",
      "quiz_ids": relevantQuizIds
    }));
  };

  globalNotificationSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    // The consumer will send us { quiz_id: X, active_users: Y }
    const quizId = data.quiz_id;
    const activeUsers = data.active_users;

    // Find the <span> for this quiz and update it
    const countSpan = document.getElementById(`quizUserCounterId${quizId}`);
    if (countSpan) {
      countSpan.textContent = activeUsers;
    }
  };

  globalNotificationSocket.onclose = function(e) {
    console.log("Category WebSocket closed.");
  };
});

// Toggle extended quiz info
function toggleMoreInfo(quizId) {
  const extendedDiv = document.getElementById(`extended-${quizId}`);
  if (extendedDiv.style.display === 'none' || !extendedDiv.style.display) {
    extendedDiv.style.display = 'block';
  } else {
    extendedDiv.style.display = 'none';
  }
}

// Simulate subscribe/unsubscribe
const subscribeBtn = document.getElementById('subscribeBtn');
let subscribed = false;
if(subscribeBtn) {
  subscribeBtn.addEventListener('click', function() {
    subscribed = !subscribed;
    subscribeBtn.textContent = subscribed ? 'Unsubscribe' : 'Subscribe to Category';
    subscribeBtn.style.backgroundColor = subscribed ? 'green' : 'var(--color-primary)';
  });
}