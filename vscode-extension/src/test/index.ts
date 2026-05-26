import Mocha from "mocha";
import { glob } from "glob";
import * as path from "path";


export async function run(): Promise<void> {
  const mocha = new Mocha({
    ui: "tdd",
    color: true,
  });

  const testsRoot = path.resolve(__dirname, "suite");

  const files = await glob("**/*.test.js", { cwd: testsRoot });

  for (const file of files) {
    mocha.addFile(path.resolve(testsRoot, file));
  }

  return new Promise((resolve, reject) => {
    mocha.run((failures) => {
      if (failures > 0) {
        reject(new Error(`${failures} tests failed.`))
      }else{
        resolve();
      }
    });
  });
}

run().catch((err) => {
  console.error("Test runner failed", err);
  process.exit(1);
});
