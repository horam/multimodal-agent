import * as assert from "assert";
import * as vscode from "vscode";
import * as sinon from "sinon";
import * as serverClient from "../../api/serverClient.js";

suite("Explain Code – Offline Fallback", () => {
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

  test("explains code locally when server is offline", async () => {
    const ext = vscode.extensions.getExtension("horam.multimodal-agent");
    assert.ok(ext, "Extension not found");
    await ext.activate();

    // Open a Dart file
    const doc = await vscode.workspace.openTextDocument({
      content: "class A {}",
      language: "dart",
    });
    await vscode.window.showTextDocument(doc);

    await vscode.commands.executeCommand("multimodalAgent.explain");

    const editor = vscode.window.activeTextEditor;
    assert.ok(editor, "No editor opened");

    const text = editor.document.getText();
    assert.ok(
      text.toLowerCase().includes("class a"),
      "Explanation missing code context",
    );
  });
});
