import * as vscode from "vscode";
import axios from "axios";
import { post } from "../api/serverClient";
import { toSnakeCase, useCaseFallback } from "./fallback";
import * as fs from "fs";
import * as path from "path";

function isServerDown(err: unknown): boolean {
  return axios.isAxiosError(err) && err.code === "ECONNREFUSED";
}

export async function generateUseCase() {
  const name = await vscode.window.showInputBox({
    prompt: "UseCase name",
    placeHolder: "e.g. FetchUser, CreateOrder",
    validateInput: (value) =>
      /^[A-Za-z][A-Za-z0-9_]*$/.test(value)
        ? null
        : "UseCase name must start with a letter",
  });
  if (!name) return;

  const entity = await vscode.window.showInputBox({
    prompt: "Entity name (optional)",
    placeHolder: "e.g. User",
  });

  const projectRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
  if (!projectRoot) {
    vscode.window.showErrorMessage("No workspace folder found.");
    return;
  }

  await vscode.window.withProgress(
    {
      location: vscode.ProgressLocation.Notification,
      title: `Generating usecase ${name}…`,
      cancellable: false,
    },
    async () => {
      try {
        const result = await post<{ code: string; path?: string }>(
          "/generate/usecase",
          {
            name,
            entity,
            project_root: projectRoot,
          },
        );

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
        if (isServerDown(err)) {
          vscode.window.showWarningMessage(
            "Server is not running. Generated a local fallback usecase stub.",
          );

          const code = useCaseFallback(name, entity);
          const snake = toSnakeCase(name);
          const outDir = path.join(projectRoot, "lib", "usecases");
          const outPath = path.join(outDir, `${snake}.dart`);

          fs.mkdirSync(outDir, { recursive: true });
          fs.writeFileSync(outPath, code, "utf8");

          const doc = await vscode.workspace.openTextDocument(outPath);
          await vscode.window.showTextDocument(doc, { preview: false });
        }
      }
    },
  );
}
