"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.generateRepository = generateRepository;
const vscode = __importStar(require("vscode"));
const serverClient_1 = require("../api/serverClient");
async function generateRepository() {
    const name = await vscode.window.showInputBox({
        prompt: "Repository name",
        placeHolder: "e.g. UserRepository, ProductRepository",
        validateInput: (value) => /^[A-Za-z][A-Za-z0-9_]*$/.test(value)
            ? null
            : "Repository name must start with a letter and be a valid Dart identifier",
    });
    if (!name)
        return;
    const entity = await vscode.window.showInputBox({
        prompt: "Entity name (optional)",
        placeHolder: "e.g. User, Product",
    });
    const description = await vscode.window.showInputBox({
        prompt: "Optional description",
        placeHolder: "Describe responsibilities, storage, API, etc.",
    });
    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: `Generating repository ${name}…`,
        cancellable: false,
    }, async () => {
        const result = await (0, serverClient_1.post)("/generate/repository", {
            name,
            entity,
            description,
        });
        const doc = await vscode.workspace.openTextDocument({
            language: "dart",
            content: result.code,
        });
        await vscode.window.showTextDocument(doc, { preview: false });
    });
}
