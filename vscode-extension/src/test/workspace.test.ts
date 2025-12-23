import * as assert from "assert";
import * as vscode from "vscode";

suite("Workspace requirements", () => {
  test("workspace folder exists", () => {
    const folders = vscode.workspace.workspaceFolders;
    assert.ok(
      folders && folders.length > 0,
      "Workspace folder is required"
    );
  });
});