import * as vscode from "vscode";
import axios from "axios";
import { post } from "../api/serverClient";
import { modelFallback } from "./fallback";

export async function generateModel() {
  const name = await vscode.window.showInputBox({ prompt: "Model name" });
  if (!name) return;

  const description = await vscode.window.showInputBox({ prompt: "Optional description" });

  const projectRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
  if (!projectRoot) {
    vscode.window.showErrorMessage("No workspace folder found.");
    return;
  }

  await vscode.window.withProgress(
    { location: vscode.ProgressLocation.Notification, title: `Generating model ${name}…` },
    async () => {
      try {
        const result = await post<{ code: string }>("/generate/model", {
          name,
          description,
          project_root: projectRoot,
        });

        const doc = await vscode.workspace.openTextDocument({ language: "dart", content: result.code });
        await vscode.window.showTextDocument(doc, { preview: false });

      } catch (err) {
        if (axios.isAxiosError(err) && err.code === "ECONNREFUSED") {
          vscode.window.showWarningMessage("Server offline — generated fallback model.");
          const doc = await vscode.workspace.openTextDocument({
            language: "dart",
            content: modelFallback(name),
          });
          await vscode.window.showTextDocument(doc, { preview: false });
        }
      }
    }
  );
}