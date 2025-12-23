import { assertCommandRegistered } from "../utils";

suite("Chat UI", () => {
  test("command is registered", async () => {
    await assertCommandRegistered("multimodalAgent.chat");
  });
});