import * as assert from "assert";
import * as vscode from "vscode";
import * as sinon from "sinon";
import * as fs from "fs";
import * as path from "path";
import axios from "axios";
import * as serverClient from "../../api/serverClient";

suite("Generate Screen – Offline Fallback", () => {
  let postStub: sinon.SinonStub;

  setup(async () => {
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

  test("writes screen fallback when server is offline", async () => {
    // Activate extension
    const ext = vscode.extensions.getExtension("horam.multimodal-agent");
    assert.ok(ext);
    await ext.activate();

    // Mock inputs
    const inputStub = sinon.stub(vscode.window, "showInputBox");
    inputStub.onFirstCall().resolves("DemoScreen"); // screen name
    inputStub.onSecondCall().resolves(undefined);   // description

    // Run command
    await vscode.commands.executeCommand(
      "multimodalAgent.generateScreen"
    );

    inputStub.restore();

    // Workspace root
    const root = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    assert.ok(root, "Workspace not found");

    const expectedPath = path.join(
      root,
      "lib",
      "screens",
      "demo_screen.dart"
    );


    // Assert file written
    assert.ok(
      fs.existsSync(expectedPath),
      "Fallback screen file was not written"
    );

    const content = fs.readFileSync(expectedPath, "utf8");

    // Assert Dart content
    assert.ok(
      content.includes("class DemoScreen extends StatelessWidget"),
      "Screen class not generated correctly"
    );

    assert.ok(
      content.includes("Scaffold"),
      "Screen scaffold missing"
    );

    // Assert editor opened correct file
    const editor = vscode.window.activeTextEditor;
    assert.ok(editor, "No editor opened");
    assert.strictEqual(
      editor.document.uri.fsPath,
      expectedPath,
      "Opened file is not the generated screen"
    );
  });
});