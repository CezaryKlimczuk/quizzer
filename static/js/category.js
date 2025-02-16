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