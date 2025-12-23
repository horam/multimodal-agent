import * as vscode from "vscode";
import axios from "axios";
import { post } from "../api/serverClient";
import { toSnakeCase, widgetFallback } from "./fallback";
import * as fs from "fs";
import * as path from "path";

function isServerDown(err: unknown): boolean {
  return axios.isAxiosError(err) && err.code === "ECONNREFUSED";
}

export async function generateWidget() {
  const name = await vscode.window.showInputBox({
    prompt: "Widget name",
    placeHolder: "e.g. ProfileCard, LoginForm",
    validateInput: (value) =>
      /^[A-Za-z][A-Za-z0-9_]*$/.test(value)
        ? null
        : "Widget name must start with a letter and be a valid Dart identifier",
  });
  if (!name) return;

  const type = await vscode.window.showQuickPick(
    [
      { label: "StatelessWidget", value: false },
      { label: "StatefulWidget", value: true },
    ],
    { placeHolder: "Select widget type" }
  );
  if (!type) return;

  const description = await vscode.window.showInputBox({
    prompt: "Optional description",
    placeHolder: "Describe layout, UI elements, behavior, etc.",
  });

  const projectRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
  if (!projectRoot) {
    vscode.window.showErrorMessage("No workspace folder found.");
    return;
  }

  await vscode.window.withProgress(
    {
      location: vscode.ProgressLocation.Notification,
      title: `Generating widget ${name}…`,
      cancellable: false,
    },
    async () => {
      try {
        const result = await post<{ code: string; path?: string }>(
          "/generate/widget",
          {
            name,
            description,
            stateful: type.value,
            project_root: projectRoot,
          }
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
            "Server is not running. Generated a local fallback widget stub."
          );

          const code = widgetFallback(name, type.value);

          const snake = toSnakeCase(name);
          const outDir = path.join(projectRoot, "lib", "widgets");
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