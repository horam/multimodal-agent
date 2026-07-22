import { spawn } from "child_process";


class AgentClient {
    constructor(private readonly executable = "agent") {}

    async run(args: string[]): Promise<string> {

        return new Promise((resolve, reject) => {
            const process = spawn(this.executable, args);
            let stdout = "";
            let stderr = "";

            process.stdout.on("data", (data) => {
                stdout += data.toString();
            });

            process.stderr.on("data", (data) => {
                stderr += data.toString();
            });

            process.on("close", (code) => {
                if (code == 0) {
                    resolve(stdout);
                } else {
                    reject(new Error(stderr));
                }
            });
        });
    }

    doctor(){
        return this.run(["doctor"]);
    }

    setup(){
        return this.run(["setup"]);
    }

    version(){
        return this.run(["version"]);
    }

    startServer(){
        return this.run(["server"]);
    }
}

export const agentClient = new AgentClient();