import * as vscode from "vscode";

import { generateWidget } from "./commands/generateWidget";
import { generateScreen } from "./commands/generateScreen";
import { generateModel } from "./commands/generateModel";
import { generateRepository } from "./commands/generateRepository";
import { generateEnum } from "./commands/generateEnum";
import { openChatPanel } from "./ui/chatPanel";

export function activate(context: vscode.ExtensionContext) {
  context.subscriptions.push(
    vscode.commands.registerCommand(
      "multimodalAgent.chat",
      ()=> openChatPanel(context)
    ),
    vscode.commands.registerCommand(
      "multimodalAgent.generateWidget",
      generateWidget
    ),
    vscode.commands.registerCommand(
      "multimodalAgent.generateScreen",
      generateScreen
    ),
    vscode.commands.registerCommand(
      "multimodalAgent.generateModel",
      generateModel
    ),
    vscode.commands.registerCommand(
      "multimodalAgent.generateRepository",
      generateRepository
    ),
    vscode.commands.registerCommand(
      "multimodalAgent.generateEnum",
      generateEnum
    ),
  );
}

export function deactivate() {}