import { io } from "socket.io-client";

// ❌ Wrong (browser can't resolve backend:5000)
// const socket = io("http://backend:5000");

//  Correct (will go through Nginx at the same domain as frontend)
const socket = io({
  path: "/socket.io/",
});

document.getElementById("feedbackForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const name = document.getElementById("name").value;
  const message = document.getElementById("message").value;

  // POST feedback
  await fetch(`/api/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, message })
  });

  document.getElementById("message").value = "";
});

async function loadFeedback() {
  const res = await fetch(`/api/feedback`);
  const feedbacks = await res.json();
  feedbacks.forEach(addFeedback);
}

function addFeedback(feedback) {
  const li = document.createElement("li");
  li.textContent = `${feedback.name}: ${feedback.message}`;
  document.getElementById("feedbackList").appendChild(li);
}

// Listen for new feedback via Socket.IO
socket.on("new_feedback", (feedback) => addFeedback(feedback));

loadFeedback();
