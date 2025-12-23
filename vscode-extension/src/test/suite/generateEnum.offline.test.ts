import * as assert from "assert";
import * as vscode from "vscode";
import * as sinon from "sinon";
import axios from "axios";
import * as serverClient from "../../api/serverClient";


suite("Generate Enum – Offline Fallback", () => {
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

  test("generates enum fallback when server is offline", async () => {
    // Ensure extension is active
    const ext = vscode.extensions.getExtension("horam.multimodal-agent");
    assert.ok(ext, "Extension not found");
    await ext.activate();

    // Mock user inputs
    const inputStub = sinon.stub(vscode.window, "showInputBox");
    inputStub.onFirstCall().resolves("Temp");       // enum name
    inputStub.onSecondCall().resolves(undefined);   // no values

    // Execute command
    await vscode.commands.executeCommand(
      "multimodalAgent.generateEnum"
    );

    inputStub.restore();

    // Assert an editor opened
    const editor = vscode.window.activeTextEditor;
    assert.ok(editor, "No editor opened");

    const text = editor.document.getText();

    // Assert fallback enum structure
    assert.ok(text.includes("enum Temp"), "Enum name missing");
    assert.ok(text.includes("value1"), "Fallback value1 missing");
    assert.ok(text.includes("value2"), "Fallback value2 missing");
    assert.ok(text.includes("value3"), "Fallback value3 missing");
  });
});