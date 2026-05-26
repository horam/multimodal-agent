import { assertCommandRegistered } from "../utils.js";

suite("Chat UI", () => {
  test("command is registered", async () => {
    await assertCommandRegistered("multimodalAgent.chat");
  });
});
