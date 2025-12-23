import * as vscode from "vscode";
import { post } from "../api/serverClient";
import { enumFallback, toSnakeCase } from "./fallback";
import axios from "axios";
import * as fs from "fs";
import * as path from "path";


function isServerDown(err: unknown): boolean {
  return axios.isAxiosError(err) && err.code === "ECONNREFUSED";
}
export async function generateEnum() {
  const name = await vscode.window.showInputBox({
    prompt: "Enum name",
    placeHolder: "e.g. UserRole, OrderStatus",
    validateInput: (value) =>
      /^[A-Za-z][A-Za-z0-9_]*$/.test(value)
        ? null
        : "Enum name must start with a letter and be a valid Dart identifier",
  });
  if (!name) return;

  const valuesInput = await vscode.window.showInputBox({
    prompt: "Enum values (comma-separated)",
    placeHolder: "e.g. pending, paid, shipped",
  });

  const values = valuesInput
    ? valuesInput.split(",").map((v) => v.trim()).filter(Boolean)
    : undefined;

  const projectRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
  if (!projectRoot) {
    vscode.window.showErrorMessage("No workspace folder found.");
    return;
  }

  await vscode.window.withProgress(
    {
      location: vscode.ProgressLocation.Notification,
      title: `Generating enum ${name}…`,
      cancellable: false,
    },
    async () => {
      try {
        const result = await post<{ code: string; path?: string }>(
          "/generate/enum",
          {
            name,
            values,
            project_root: projectRoot,
          }
        );

        if (result.path) {
            const doc = await vscode.workspace.openTextDocument(result.path);
            await vscode.window.showTextDocument(doc);
          } else {
            const doc = await vscode.workspace.openTextDocument({
              language: "dart",
              content: result.code,
              });
            await vscode.window.showTextDocument(doc);
          }

      } catch (err: unknown) {
        // Server is down → client-side fallback
        if (isServerDown(err)) {
          vscode.window.showWarningMessage(
            "Server is not running. Generated a local fallback enum stub."
          );

          const code = enumFallback(name, values);
          const snake = toSnakeCase(name);
          const enumDir = path.join(projectRoot, "lib", "enums");
          const outPath = path.join(enumDir, `${snake}.dart`);

          fs.mkdirSync(enumDir, { recursive: true });
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