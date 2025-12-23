import * as path from "path";
import * as os from "os";
import * as fs from "fs";
import { runTests } from "@vscode/test-electron";

function ensureDir(p: string) {
  fs.mkdirSync(p, { recursive: true });
}

async function main() {
  try {
    const extensionDevelopmentPath = path.resolve(__dirname, "../../");
    const extensionTestsPath = path.resolve(__dirname, "./index");

    const userDataDir = path.join(os.tmpdir(), "vscode-test-user-data");

    // Create a workspace folder for tests
    const workspacePath = path.join(os.tmpdir(), "multimodal-agent-test-workspace");
    ensureDir(path.join(workspacePath, "lib", "enums"));
    ensureDir(path.join(workspacePath, "lib", "models"));
    ensureDir(path.join(workspacePath, "lib", "repositories"));
    ensureDir(path.join(workspacePath, "lib", "screens"));
    ensureDir(path.join(workspacePath, "lib", "widgets"));

    await runTests({
      extensionDevelopmentPath,
      extensionTestsPath,
      launchArgs: [
        workspacePath,
        "--disable-extensions",
        `--user-data-dir=${userDataDir}`,
      ],
    });
  } catch (err) {
    console.error("Failed to run tests");
    process.exit(1);
  }
}

main();