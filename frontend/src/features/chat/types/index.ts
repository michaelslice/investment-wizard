export interface ChatMessage {role:'user'|'assistant';content:string;toolsUsed?:string[]}
export interface ChatResponse {message:string;toolsUsed:string[];model:string}
