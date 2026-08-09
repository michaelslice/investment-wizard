import type { ChatMessage, ChatResponse } from '../types';

export async function sendChat(messages:ChatMessage[]):Promise<ChatResponse>{const response=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({messages:messages.map(({role,content})=>({role,content}))})}),body=await response.json();if(!response.ok)throw new Error([body.error??body.detail??'Unable to contact research assistant',body.hint].filter(Boolean).join('. '));return body}
