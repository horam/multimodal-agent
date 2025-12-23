import * as vscode from "vscode";
import { post } from "../api/serverClient";
import { modelFallback, toSnakeCase } from "./fallback";
import axios from "axios";
import * as fs from "fs";
import * as path from "path";

function isServerDown(err: unknown): boolean {
  return axios.isAxiosError(err) && err.code === "ECONNREFUSED";
}
export async function generateModel() {
  const name = await vscode.window.showInputBox({
    prompt: "Model name",
    placeHolder: "e.g. UserProfile, InvoiceItem",
    validateInput: (value) =>
      /^[A-Za-z][A-Za-z0-9_]*$/.test(value)
        ? null
        : "Model name must start with a letter and contain only letters, numbers, or underscores",
  });

  if (!name) return;

  const description = await vscode.window.showInputBox({
    prompt: "Optional description",
    placeHolder: "Describe fields, purpose, conversions, etc.",
  });

  const projectRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
  if (!projectRoot) {
    vscode.window.showErrorMessage("No workspace folder found.");
    return;
  }

  await vscode.window.withProgress(
    {
      location: vscode.ProgressLocation.Notification,
      title: `Generating model ${name}…`,
      cancellable: false,
    },
    async () => {
      try {
        const result = await post<{ code: string; path?: string }>(
          "/generate/model",
          {
            name,
            description,
            project_root: projectRoot,
          }
        );

        // If server returns a real file path, open it. Otherwise open the content.
        if (result.path) {
          const doc = await vscode.workspace.openTextDocument(result.path);
          await vscode.window.showTextDocument(doc, { preview: false });
        } else {
          const doc = await vscode.workspace.openTextDocument({
            language: "dart",
            content: result.code,
          });
          await vscode.window.showTextDocument(doc, { preview: false });
        }
      } catch (err: unknown) {
        // Server is down → client-side fallback that writes a real file
        if (isServerDown(err)) {
          vscode.window.showWarningMessage(
            "Server is not running. Generated a local fallback model stub."
          );

          const code = modelFallback(name);

          const snake = toSnakeCase(name);
          const outDir = path.join(projectRoot, "lib", "models");
          const outPath = path.join(outDir, `${snake}.dart`);

          fs.mkdirSync(outDir, { recursive: true });
          fs.writeFileSync(outPath, code, "utf8");

          const doc = await vscode.workspace.openTextDocument(outPath);
          await vscode.window.showTextDocument(doc, { preview: false });
          return;
        }

        // other errors already shown by serverClient
      }
    }
  );
}