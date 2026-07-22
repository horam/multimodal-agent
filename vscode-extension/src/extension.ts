import * as vscode from "vscode";
import { isAgentInstalled, startServer } from "./server/serverManager";
import { generateWidget } from "./commands/generateWidget";
import { generateScreen } from "./commands/generateScreen";
import { generateModel } from "./commands/generateModel";
import { generateRepository } from "./commands/generateRepository";
import { generateEnum } from "./commands/generateEnum";
import { openChatPanel } from "./ui/chatPanel";
import { generateUseCase } from "./commands/generateUseCase";
import { refactorCode } from "./commands/refactorCode";
import { explainCode } from "./commands/explainCode";
import { setupSteps } from "./commands/setupSteps";

export async function activate(context: vscode.ExtensionContext) {
  console.log("activate()");
  context.subscriptions.push(
    vscode.commands.registerCommand("multimodalAgent.chat", () =>
      openChatPanel(),
    ),
    vscode.commands.registerCommand("multimodalAgent.setup", () => {
    console.log("register setup");
    return setupSteps();
    },
    ),
    vscode.commands.registerCommand(
      "multimodalAgent.generateWidget",
      generateWidget,
    ),
    vscode.commands.registerCommand(
      "multimodalAgent.generateScreen",
      generateScreen,
    ),
    vscode.commands.registerCommand(
      "multimodalAgent.generateModel",
      generateModel,
    ),
    vscode.commands.registerCommand(
      "multimodalAgent.generateRepository",
      generateRepository,
    ),
    vscode.commands.registerCommand(
      "multimodalAgent.generateEnum",
      generateEnum,
    ),
    vscode.commands.registerCommand(
      "multimodalAgent.generateUsecase",
      generateUseCase,
    ),
    vscode.commands.registerCommand(
      "multimodalAgent.refactorCode",
      refactorCode,
    ),
    vscode.commands.registerCommand("multimodalAgent.explainCode", explainCode),
  );

  try {
    if (!(await isAgentInstalled())) {
      vscode.window.showErrorMessage(
        "Agent is not installed. Run 'Multimodal Agent: Setup'.",
      );
    }
    await startServer(context);

    vscode.window.showInformationMessage(
      "Multimodal agent server started successfully.",
    );
  } catch (error: unknown) {
    vscode.window.showErrorMessage(`${error}`);
  }
}

export function deactivate() {}
