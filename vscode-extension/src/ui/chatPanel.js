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
exports.openChatPanel = openChatPanel;
const vscode = __importStar(require("vscode"));
const serverClient_1 = require("../api/serverClient");
const chatWebview_1 = require("./chatWebview");
function openChatPanel(context) {
    const panel = vscode.window.createWebviewPanel("multimodalAgentChat", "Agent", vscode.ViewColumn.Beside, {
        enableScripts: true,
        retainContextWhenHidden: true,
    });
    panel.webview.html = (0, chatWebview_1.getChatHtml)();
    panel.webview.onDidReceiveMessage(async (msg) => {
        if (msg.type === "send") {
            const editor = vscode.window.activeTextEditor;
            const selection = editor
                ? editor.document.getText(editor.selection)
                : undefined;
            const contextPayload = {
                language: editor?.document.languageId,
                fileName: editor?.document.fileName,
                selection,
            };
            panel.webview.postMessage({
                type: "thinking",
            });
            try {
                const resp = await (0, serverClient_1.post)("/chat", {
                    message: msg.text,
                    context: contextPayload,
                });
                panel.webview.postMessage({
                    type: "response",
                    text: resp.text,
                });
            }
            catch {
                panel.webview.postMessage({
                    type: "error",
                    text: "Agent failed to respond.",
                });
            }
        }
    });
}
