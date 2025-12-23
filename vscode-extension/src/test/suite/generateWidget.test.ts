import { assertCommandRegistered } from "../utils";

suite("Generate Widget UI", () => {
  test("command is registered", async () => {
    await assertCommandRegistered("multimodalAgent.generateWidget");
  });
});