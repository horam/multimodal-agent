"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getChatHtml = getChatHtml;
function getChatHtml() {
    return `
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<style>
  body {
    font-family: sans-serif;
    padding: 10px;
  }
  #messages {
    height: 70vh;
    overflow-y: auto;
    border: 1px solid #ddd;
    padding: 8px;
    margin-bottom: 8px;
  }
  .user { font-weight: bold; }
  .agent { color: #007acc; }
  #input {
    width: 85%;
  }
</style>
</head>
<body>

<h3>Multimodal Agent</h3>

<div id="messages"></div>

<input id="input" placeholder="Ask the agent…" />
<button id="send">▶</button>

<script>
  const vscode = acquireVsCodeApi();
  const messages = document.getElementById("messages");

  function add(role, text) {
    const div = document.createElement("div");
    div.className = role;
    div.textContent = role + ": " + text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  document.getElementById("send").onclick = () => {
    const input = document.getElementById("input");
    if (!input.value) return;

    add("You", input.value);
    vscode.postMessage({ type: "send", text: input.value });
    input.value = "";
  };

  window.addEventListener("message", (event) => {
    const msg = event.data;

    if (msg.type === "thinking") {
      add("Agent", "…");
    }

    if (msg.type === "response") {
      add("Agent", msg.text);
    }

    if (msg.type === "error") {
      add("Agent", msg.text);
    }
  });
</script>

</body>
</html>
`;
}
