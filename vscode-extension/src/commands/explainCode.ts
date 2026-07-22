import * as vscode from "vscode";
import axios from "axios";
import { post } from "../api/serverClient";

export async function explainCode() {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    vscode.window.showErrorMessage("No active editor.");
    return;
  }

  const code = editor.document.getText();

  await vscode.window.withProgress(
    {
      location: vscode.ProgressLocation.Notification,
      title: "Explaining code…",
      cancellable: false,
    },
    async () => {
      try {
        const result = await post<{ text: string }>("/explain", { code });

        vscode.window.showInformationMessage(result.text);
      } catch (err: unknown) {
        console.log("[ExplainCode full error: ", err);

        if (axios.isAxiosError(err)) {
          const message = err.response?.data?.detail ?? err.message;
          vscode.window.showErrorMessage(message);
        } else {
          vscode.window.showErrorMessage(`Command failed: ${String(err)}`);
        }
      }
    },
  );
}
