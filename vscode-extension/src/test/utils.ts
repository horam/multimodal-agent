import * as vscode from "vscode";
import * as assert from "assert";

export async function assertCommandRegistered(command: string) {
  const commands = await vscode.commands.getCommands(true);
  assert.ok(commands.includes(command), `${command} not registered`);
}

export async function assertExtensionActive() {
  const ext = vscode.extensions.getExtension("horam.multimodal-agent");
  assert.ok(ext, "Extension not found");
  await ext.activate();
  assert.ok(ext.isActive, "Extension not active");
}