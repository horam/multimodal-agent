import { assertCommandRegistered } from "../utils.js";

suite("Generate Widget UI", () => {
  test("command is registered", async () => {
    await assertCommandRegistered("multimodalAgent.generateWidget");
  });
});
