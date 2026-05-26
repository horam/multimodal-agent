import * as vscode from "vscode";
import axios from "axios";
import { post } from "../api/serverClient";

function isServerDown(err: unknown): boolean {
  return axios.isAxiosError(err) && err.code === "ECONNREFUSED";
}

export async function refactorCode() {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    vscode.window.showErrorMessage("No active editor.");
    return;
  }

  const code = editor.document.getText();

  await vscode.window.withProgress(
    {
      location: vscode.ProgressLocation.Notification,
      title: "Refactoring code…",
      cancellable: false,
    },
    async () => {
      try {
        const result = await post<{ text: string }>("/refactor", { code });

        // show result in editor (no overwrite by default)
        const doc = await vscode.workspace.openTextDocument({
          language: "dart",
          content: result.text,
        });
        await vscode.window.showTextDocument(doc, { preview: false });
      } catch (err: unknown) {
        if (isServerDown(err)) {
          vscode.window.showWarningMessage(
            "Server offline. Showing original code.",
          );

          const doc = await vscode.workspace.openTextDocument({
            language: "dart",
            content: code,
          });
          await vscode.window.showTextDocument(doc, { preview: false });
        }
      }
    },
  );
}
