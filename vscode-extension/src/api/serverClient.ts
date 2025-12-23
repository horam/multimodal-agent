import axios, { AxiosError } from "axios";
import * as vscode from "vscode";

const DEFAULT_TIMEOUT_MS = 60_000;

export function getServerUrl(): string {
  const url = vscode.workspace
    .getConfiguration("multimodalAgent")
    .get<string>("serverUrl");

    if(!url){
        throw new Error(
              "Multimodal Agent server URL is not configured. Please set multimodalAgent.serverUrl in settings."
        )
    }

    return url.replace(/\/$/, "");
}

export async function post<T>(path: string, payload: unknown): Promise<T> {
    let url: string;
    try {
         url = `${getServerUrl()}${path}`;
    }catch(error){
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

        return response.data;
        } catch (error) {
        handleAxiosError(error, path);
        throw error;
    }
}


function handleAxiosError(error: unknown, path: string){
    if (axios.isAxiosError(error)){
        const axiosError = error as AxiosError<any>;
        const message = axiosError.response?.data?.detail ||  axiosError.response?.statusText || axiosError.message;
        vscode.window.showErrorMessage(
            `Multimodal Agent error (${path}): ${message}`
        )

    }else{
        vscode.window.showErrorMessage(
            `Unexpected error while calling Multimodal Agent (${path})`
        );
    }
}