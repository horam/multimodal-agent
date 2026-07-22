import axios from "axios";
import type { AxiosError } from "axios";
import * as vscode from "vscode";

const DEFAULT_TIMEOUT_MS = 60_000;

export function getServerUrl(): string {
  const url = vscode.workspace
    .getConfiguration("multimodalAgent")
    .get<string>("serverUrl");

  if (!url) {
    throw new Error(
      "Multimodal Agent server URL is not configured. Please set multimodalAgent.serverUrl in settings.",
    );
  }

  return url.replace(/\/$/, "");
}

export async function post<T>(path: string, payload: unknown): Promise<T> {
  let url: string;
  console.log(`[Agent] sending request to server`);
  try {
    url = `${getServerUrl()}${path}`;
  } catch (error) {
    vscode.window.showErrorMessage((error as Error).message);
    throw error;
  }
  try {
    const response = await axios.post<T>(url, payload, {
      timeout: DEFAULT_TIMEOUT_MS,
      headers: {
        "Content-Type": "application/json",
      },
    });
    console.log("[Agent] response received successfully", response);

    return response.data;
  } catch (error) {
    console.log("[Agent] error during request:", error);
    handleAxiosError(error, path);
    throw error;
  }
}

function handleAxiosError(error: unknown, path: string) {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<{ detail?: string }>;
    const message =
      axiosError.response?.data?.detail ||
      axiosError.response?.statusText ||
      axiosError.message;
    vscode.window.showErrorMessage(
      `Multimodal Agent error (${path}): ${message}`,
    );
  } else {
    vscode.window.showErrorMessage(
      `Unexpected error while calling Multimodal Agent (${path})`,
    );
  }
}
