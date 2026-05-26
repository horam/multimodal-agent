import { assertCommandRegistered } from "../utils.js";

suite("Generate Screen UI", () => {
  test("command is registered", async () => {
    await assertCommandRegistered("multimodalAgent.generateScreen");
  });
});
