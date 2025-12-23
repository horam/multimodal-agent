import { assertCommandRegistered } from "../utils";

suite("Generate Screen UI", () => {
  test("command is registered", async () => {
    await assertCommandRegistered("multimodalAgent.generateScreen");
  });
});