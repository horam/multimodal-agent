import { assertCommandRegistered } from "../utils.js";

suite("Generate Model UI", () => {
  test("command is registered", async () => {
    await assertCommandRegistered("multimodalAgent.generateModel");
  });
});
