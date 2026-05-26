import * as vscode from "vscode";
import axios from "axios";
import { post } from "../api/serverClient";

function isServerDown(err: unknown): boolean {
  return axios.isAxiosError(err) && err.code === "ECONNREFUSED";
}

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
        if (isServerDown(err)) {
          vscode.window.showInformationMessage(
            "OFFLINE: Unable to explain code. Server not running.",
          );
        }
      }
    },
  );
}
