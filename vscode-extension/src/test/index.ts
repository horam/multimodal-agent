import Mocha from "mocha";
import { glob } from "glob";
import * as path from "path";

export function run(): Promise<void> {
  const mocha = new Mocha({
    ui: "tdd",
    color: true,
  });

  const testsRoot = path.resolve(__dirname, "suite");

  return new Promise((resolve, reject) => {
    glob("**/*.test.js", { cwd: testsRoot })
      .then((files) => {
        files.forEach((f) =>
          mocha.addFile(path.resolve(testsRoot, f))
        );

        mocha.run((failures) => {
          failures > 0
            ? reject(new Error(`${failures} tests failed.`))
            : resolve();
        });
      })
      .catch(reject);
  });
}