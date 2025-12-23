import * as assert from "assert";
import * as vscode from "vscode";
import * as sinon from "sinon";
import * as fs from "fs";
import * as path from "path";

import * as serverClient from "../../api/serverClient";

suite("Generate Model – Offline Fallback", () => {
  let postStub: sinon.SinonStub;

  setup(() => {
    postStub = sinon.stub(serverClient, "post").rejects(
      Object.assign(new Error("ECONNREFUSED"), {
        isAxiosError: true,
        code: "ECONNREFUSED",
      })
    );
  });

  teardown(() => {
    postStub.restore();
  });

  test("writes model fallback to lib/models when server is offline", async () => {
    // Activate extension
    const ext = vscode.extensions.getExtension("horam.multimodal-agent");
    assert.ok(ext, "Extension not found");
    await ext.activate();

    // Mock inputs
    const inputStub = sinon.stub(vscode.window, "showInputBox");
    inputStub.onFirstCall().resolves("UserProfile"); // model name
    inputStub.onSecondCall().resolves(undefined);    // description

    // Run command
    await vscode.commands.executeCommand(
      "multimodalAgent.generateModel"
    );

    inputStub.restore();

    // Workspace root
    const root = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    assert.ok(root, "Workspace not found");

    const expectedPath = path.join(
      root,
      "lib",
      "models",
      "user_profile.dart"
    );

    // Assert file written
    assert.ok(
      fs.existsSync(expectedPath),
      "Fallback model file was not written"
    );

    const content = fs.readFileSync(expectedPath, "utf8");

    // Assert Dart content
    assert.ok(
      content.includes("class UserProfile"),
      "Model class not generated correctly"
    );

    // Assert editor opened the same file
    const editor = vscode.window.activeTextEditor;
    assert.ok(editor, "No editor opened");
    assert.strictEqual(
      editor.document.uri.fsPath,
      expectedPath,
      "Opened file is not the generated model"
    );
  });
});