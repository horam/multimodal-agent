import * as assert from "assert";
import * as vscode from "vscode";
import { assertCommandRegistered, assertExtensionActive } from "../utils.js";

suite("Generate UseCase UI", () => {
  test("command is registered", async () => {
    await assertCommandRegistered("multimodalAgent.generateUseCase");
  });

  test("workspace is available", () => {
    assert.ok(vscode.workspace.workspaceFolders?.length);
  });

  test("extension activates", async () => {
    await assertExtensionActive();
  });
});
