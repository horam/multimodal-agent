import * as assert from "assert";
import * as vscode from "vscode";
import * as sinon from "sinon";
import * as fs from "fs";
import * as path from "path";

import * as serverClient from "../../api/serverClient";

type WidgetPick = { label: string; value: boolean };

suite("Generate Widget – Offline Fallback", () => {
  let postStub: sinon.SinonStub;
  let pickStub: sinon.SinonStub;
  let inputStub: sinon.SinonStub;

  setup(() => {
    // Simulate server being offline
    postStub = sinon.stub(serverClient, "post").rejects(
      Object.assign(new Error("ECONNREFUSED"), {
        isAxiosError: true,
        code: "ECONNREFUSED",
      })
    );

    // Stub quick pick (Stateless / Stateful)
    pickStub = sinon.stub(
      vscode.window,
      "showQuickPick"
    ) as unknown as sinon.SinonStub<
      [
        readonly WidgetPick[] | Thenable<readonly WidgetPick[]>,
        vscode.QuickPickOptions | undefined
      ],
      Thenable<WidgetPick | undefined>
    >;

    // Stub input boxes
    inputStub = sinon.stub(vscode.window, "showInputBox");
  });

  teardown(() => {
    postStub.restore();
    pickStub.restore();
    inputStub.restore();
  });

  test("writes stateless widget fallback when server is offline", async () => {
    // Activate extension
    const ext = vscode.extensions.getExtension("horam.multimodal-agent");
    assert.ok(ext, "Extension not found");
    await ext.activate();

    // Mock inputs
    inputStub.onFirstCall().resolves("IconWidget"); // widget name
    inputStub.onSecondCall().resolves(undefined);   // description
    pickStub.resolves({ label: "StatelessWidget", value: false });

    // Execute command
    await vscode.commands.executeCommand(
      "multimodalAgent.generateWidget"
    );

    const root = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    assert.ok(root, "Workspace not found");

    const expectedPath = path.join(
      root,
      "lib",
      "widgets",
      "icon_widget.dart"
    );

    // Assert file exists
    assert.ok(
      fs.existsSync(expectedPath),
      "Fallback stateless widget file was not written"
    );

    const content = fs.readFileSync(expectedPath, "utf8");

    // Assert Dart content
    assert.ok(
      content.includes("class IconWidget extends StatelessWidget"),
      "StatelessWidget not generated correctly"
    );

    // Assert editor opened correct file
    const editor = vscode.window.activeTextEditor;
    assert.ok(editor, "No editor opened");
    assert.strictEqual(
      editor.document.uri.fsPath,
      expectedPath,
      "Opened file is not the generated widget"
    );
  });

  test("writes stateful widget fallback when server is offline", async () => {
    // Activate extension
    const ext = vscode.extensions.getExtension("horam.multimodal-agent");
    assert.ok(ext, "Extension not found");
    await ext.activate();

    // Mock inputs
    inputStub.onFirstCall().resolves("UserName");   // widget name
    inputStub.onSecondCall().resolves(undefined);  // description
    pickStub.resolves({ label: "StatefulWidget", value: true });

    // Execute command
    await vscode.commands.executeCommand(
      "multimodalAgent.generateWidget"
    );

    const root = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    assert.ok(root, "Workspace not found");

    const expectedPath = path.join(
      root,
      "lib",
      "widgets",
      "user_name.dart"
    );

    // Assert file exists
    assert.ok(
      fs.existsSync(expectedPath),
      "Fallback stateful widget file was not written"
    );

    const content = fs.readFileSync(expectedPath, "utf8");

    // Assert Dart content
    assert.ok(
      content.includes("class UserName extends StatefulWidget"),
      "StatefulWidget not generated correctly"
    );

    assert.ok(
      content.includes("class _UserNameState"),
      "State class not generated"
    );
  });
});