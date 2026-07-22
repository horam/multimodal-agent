import type * as vscode from "vscode";
import axios from "axios";
import type { ChildProcess } from "child_process";
import { spawn } from "child_process";
import { ensureAgentIsInstalled } from "../environmentManager";
let serverProcess: ChildProcess | undefined;

const SERVER_URL = "http://127.0.0.1:8000";

export async function startServer(
  context: vscode.ExtensionContext,
): Promise<void> {
  if (await isServerRunning()) {
    return;
  }

  const SERVER_COMMAND = await ensureAgentIsInstalled(context);
  const SERVER_ARGS = ["server", "--port", "8000"];

  serverProcess = spawn(SERVER_COMMAND, SERVER_ARGS, {
    detached: false,
  });

  serverProcess.stdout?.on("data", (data) => {
    console.log(`[agent]: ${data}`);
  });

  serverProcess.stderr?.on("data", (data) => {
    console.error(`[agent]: ${data}`);
  });

  serverProcess.on("error", (err) => {
    console.error("[agent]", err);
  });

  serverProcess.on("exit", (code, signal) => {
    console.error(`[agent] code=${code} signal=${signal}`);
  });

  await waitForServer();
}

async function isServerRunning(): Promise<boolean> {
  try {
    await axios.get(`${SERVER_URL}/health`, {
      timeout: 2000,
    });
    return true;
  } catch {
    return false;
  }
}

async function waitForServer(timeoutMs = 15000): Promise<void> {
  const startTime = Date.now();
  while (Date.now() - startTime < timeoutMs) {
    if (await isServerRunning()) {
      return;
    }
    await new Promise((resolve) => setTimeout(resolve, 500));
  }
  throw new Error("Server failed to start");
}

export async function isAgentInstalled(): Promise<boolean> {
  return new Promise((resolve) => {
    const process = spawn("agent", ["--help"]);
    process.on("error", () => resolve(false));
    process.on("exit", (code) => resolve(code === 0));
  });
}
