import * as path from "path";
import * as os from "os";
import * as fs from "fs";
import { runTests } from "@vscode/test-electron";

function ensureDir(p: string) {
  fs.mkdirSync(p, { recursive: true });
}

async function main() {
  const extensionDevelopmentPath = path.resolve(__dirname, "../../");
  const extensionTestsPath = path.resolve(__dirname, "./index.js");

  const userDataDir = path.join(os.tmpdir(), "vscode-test-user-data");

  const workspacePath = path.join(
    os.tmpdir(),
    "multimodal-agent-test-workspace",
  );

  ensureDir(path.join(workspacePath, "lib", "enums"));
  ensureDir(path.join(workspacePath, "lib", "models"));
  ensureDir(path.join(workspacePath, "lib", "repositories"));
  ensureDir(path.join(workspacePath, "lib", "screens"));
  ensureDir(path.join(workspacePath, "lib", "widgets"));
  ensureDir(path.join(workspacePath, "lib", "usecases"));


  await runTests({
    extensionDevelopmentPath,
    extensionTestsPath,
    launchArgs: [
      workspacePath,
      "--disable-extensions",
      "--disable-workspace-trust",
      "--skip-welcome",
      "--skip-release-notes",
      "--disable-telemetry",
      "--disable-updates",
      `--user-data-dir=${userDataDir}`,
    ],
  });
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});