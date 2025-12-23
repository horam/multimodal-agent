import { assertCommandRegistered } from "../utils";

suite("Generate Model UI", () => {
  test("command is registered", async () => {
    await assertCommandRegistered("multimodalAgent.generateModel");
  });
});