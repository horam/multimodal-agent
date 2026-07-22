import * as vscode from "vscode";
import { spawn } from "child_process";
import * as path from "path";
import * as fs from "fs";

function runCommand(command: string, args: string[]): Promise<void> {
  return new Promise((resolve, reject) => {
    const process = spawn(command, args);

    process.stdout.on("data", (data) => {
      console.log(`[python]: ${data}`);
    });
    process.stderr.on("data", (data) => {
      console.error(`[python]: ${data}`);
    });

    process.on("close", (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`${command} failed with exit code ${code}`));
      }
    });
  });
}

export async function ensureAgentIsInstalled(context: vscode.ExtensionContext) {
  const extensionDir = context.globalStorageUri.fsPath;

  const venvPath = path.join(extensionDir, ".venv");

  const agentPath = path.join(venvPath, "bin", "agent");

  if (fs.existsSync(agentPath)) {
    return agentPath;
  }

  fs.mkdirSync(extensionDir, { recursive: true });

  vscode.window.showInformationMessage("Installing agent...");

  await runCommand("python3", ["-m", "venv", venvPath]);

  const pipPath = path.join(venvPath, "bin", "pip");

  await runCommand(pipPath, ["install", "--upgrade", "pip"]);

  await runCommand(pipPath, ["install", "multimodal-agent"]);

  vscode.window.showInformationMessage("Agent installed successfully.");

  return agentPath;
}
