import * as assert from "assert";
import * as vscode from "vscode";
import * as sinon from "sinon";
import * as serverClient from "../../api/serverClient.js";

suite("Refactor Code – Offline Fallback", () => {
  let postStub: sinon.SinonStub;

  setup(() => {
    postStub = sinon.stub(serverClient, "post").rejects(
      Object.assign(new Error("ECONNREFUSED"), {
        isAxiosError: true,
        code: "ECONNREFUSED",
      }),
    );
  });

  teardown(() => {
    postStub.restore();
  });

  test("keeps code intact when server is offline", async () => {
    // Activate extension
    const ext = vscode.extensions.getExtension("horam.multimodal-agent");
    assert.ok(ext, "Extension not found");
    await ext.activate();

    // Open Dart file
    const doc = await vscode.workspace.openTextDocument({
      content: "class A {}",
      language: "dart",
    });
    await vscode.window.showTextDocument(doc);

    // Execute refactor
    await vscode.commands.executeCommand("multimodalAgent.refactor");

    // Assert editor content
    const editor = vscode.window.activeTextEditor;
    assert.ok(editor, "No editor opened");

    const text = editor.document.getText();

    // Offline behavior = no destructive change
    assert.ok(text.includes("class A"), "Original class missing");
  });
});
