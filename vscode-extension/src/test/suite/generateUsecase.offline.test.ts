import * as assert from "assert";
import * as vscode from "vscode";
import * as sinon from "sinon";
import * as serverClient from "../../api/serverClient.js";

suite("Generate UseCase – Offline Fallback", () => {
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

  test("generates usecase fallback when server is offline", async () => {
    // Activate extension
    const ext = vscode.extensions.getExtension("horam.multimodal-agent");
    assert.ok(ext, "Extension not found");
    await ext.activate();

    // Mock user inputs
    const inputStub = sinon.stub(vscode.window, "showInputBox");
    inputStub.onFirstCall().resolves("FetchUser"); // UseCase name
    inputStub.onSecondCall().resolves("User"); // Entity name

    // Execute command
    await vscode.commands.executeCommand("multimodalAgent.generateUseCase");

    inputStub.restore();

    // Assert editor opened
    const editor = vscode.window.activeTextEditor;
    assert.ok(editor, "No editor opened");

    const text = editor.document.getText();

    // Assertions — fallback UseCase structure
    assert.ok(text.includes("class FetchUser"), "UseCase class missing");
    assert.ok(text.includes("call()"), "call() method missing");
    assert.ok(text.includes("Future"), "Future return type missing");

    // Safety checks
    assert.ok(!text.includes("```"), "Markdown leaked into output");
    assert.ok(!text.includes("<html>"), "HTML leaked into output");
  });
});
