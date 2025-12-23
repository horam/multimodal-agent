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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getServerUrl = getServerUrl;
exports.post = post;
const axios_1 = __importDefault(require("axios"));
const vscode = __importStar(require("vscode"));
const DEFAULT_TIMEOUT_MS = 15000;
function getServerUrl() {
    const url = vscode.workspace
        .getConfiguration("multimodalAgent")
        .get("serverUrl");
    if (!url) {
        throw new Error("Multimodal Agent server URL is not configured. Please set multimodalAgent.serverUrl in settings.");
    }
    return url.replace(/\/$/, "");
}
async function post(path, payload) {
    let url;
    try {
        url = `${getServerUrl()}${path}`;
    }
    catch (error) {
        vscode.window.showErrorMessage(error.message);
        throw error;
    }
    try {
        const response = await axios_1.default.post(url, payload, {
            timeout: DEFAULT_TIMEOUT_MS,
            headers: {
                "Content-Type": "application/json",
            },
        });
        return response.data;
    }
    catch (error) {
        handleAxiosError(error, path);
        throw error;
    }
}
function handleAxiosError(error, path) {
    if (axios_1.default.isAxiosError(error)) {
        const axiosError = error;
        const message = axiosError.response?.data?.detail || axiosError.response?.statusText || axiosError.message;
        vscode.window.showErrorMessage(`Multimodal Agent error (${path}): ${message}`);
    }
    else {
        vscode.window.showErrorMessage(`Unexpected error while calling Multimodal Agent (${path})`);
    }
}
