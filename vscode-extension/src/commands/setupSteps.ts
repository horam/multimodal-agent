import * as vscode from "vscode";

export async function setupSteps() {
  console.log("register setup");
  return vscode.window.showInformationMessage(
    "\n1. pip install multimodal-agent \n2. agent config \n3. Reload VS Code",
  );
}
