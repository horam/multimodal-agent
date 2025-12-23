import * as vscode from "vscode";
import axios from "axios";
import { post } from "../api/serverClient";
import { repositoryFallback, toSnakeCase } from "./fallback";
import * as fs from "fs";
import * as path from "path";

function isServerDown(err: unknown): boolean {
  return axios.isAxiosError(err) && err.code === "ECONNREFUSED";
}

export async function generateRepository() {
  const name = await vscode.window.showInputBox({
    prompt: "Repository name",
    placeHolder: "e.g. UserRepository, ProductRepository",
    validateInput: (value) =>
      /^[A-Za-z][A-Za-z0-9_]*$/.test(value)
        ? null
        : "Repository name must start with a letter and be a valid Dart identifier",
  });
  if (!name) return;

  const entity = await vscode.window.showInputBox({
    prompt: "Entity name (optional)",
    placeHolder: "e.g. User, Product",
  });

  const description = await vscode.window.showInputBox({
    prompt: "Optional description",
    placeHolder: "Describe responsibilities, storage, API, etc.",
  });

  const projectRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
  if (!projectRoot) {
    vscode.window.showErrorMessage("No workspace folder found.");
    return;
  }

  await vscode.window.withProgress(
    {
      location: vscode.ProgressLocation.Notification,
      title: `Generating repository ${name}…`,
      cancellable: false,
    },
    async () => {
      try {
        const result = await post<{ code: string; path?: string }>(
          "/generate/repository",
          {
            name,
            entity,
            description,
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
            "Server is not running. Generated a local fallback repository stub."
          );

          const code = repositoryFallback(name, entity);

          const snake = toSnakeCase(name);
          const outDir = path.join(projectRoot, "lib", "repositories");
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