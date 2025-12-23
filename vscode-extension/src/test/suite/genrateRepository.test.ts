import { assertCommandRegistered } from "../utils";

suite("Generate Repository UI", () => {
  test("command is registered", async () => {
    await assertCommandRegistered("multimodalAgent.generateRepository");
  });
});