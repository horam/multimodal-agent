import * as vscode from "vscode";
import { post } from "../api/serverClient";
import { getChatHtml } from "./chatWebview";


const sessionId = crypto.randomUUID();

export function openChatPanel(context: vscode.ExtensionContext) {
  const panel = vscode.window.createWebviewPanel(
    "multimodalAgentChat",
    "Agent",
    vscode.ViewColumn.Beside,
    {
      enableScripts: true,
      retainContextWhenHidden: true,
    }
  );

  panel.webview.html = getChatHtml();

  panel.webview.onDidReceiveMessage(async (msg) => {
    if (msg.type === "send") {
      const editor = vscode.window.activeTextEditor;

      const selection = editor
        ? editor.document.getText(editor.selection)
        : undefined;

      const contextPayload = {
        language: editor?.document.languageId,
        fileName: editor?.document.fileName,
        selection,
      };

      panel.webview.postMessage({
        type: "thinking",
        id: "pending",
      });

      try {
        const resp = await post<{ text: string }>("/chat", {
          message: msg.text,
          session_id: sessionId,
          context: contextPayload,
        });

        panel.webview.postMessage({
          type: "response",
          text: resp.text,
        });
      } catch {
        panel.webview.postMessage({
          type: "error",
          text: "Agent failed to respond.",
        });
      }
    }
  });
}