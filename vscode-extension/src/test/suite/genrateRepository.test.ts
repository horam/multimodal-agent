import { assertCommandRegistered } from "../utils.js";

suite("Generate Repository UI", () => {
  test("command is registered", async () => {
    await assertCommandRegistered("multimodalAgent.generateRepository");
  });
});
