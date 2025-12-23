import * as assert from "assert";
import * as vscode from "vscode";

suite("Extension activation", () => {
  test("Extension should activate", async () => {
    const ext = vscode.extensions.getExtension("horam.multimodal-agent");
    assert.ok(ext, "Extension not found");

    await ext?.activate();
    assert.ok(ext?.isActive, "Extension failed to activate");
  });
});