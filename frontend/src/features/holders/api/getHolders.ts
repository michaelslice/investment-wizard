import type { HoldersResponse } from '../types';
export async function getHolders(symbol:string):Promise<HoldersResponse>{const response=await fetch(`/api/research/holders/${encodeURIComponent(symbol)}`),body=await response.json();if(!response.ok)throw new Error(body.error??body.detail??'Unable to load holders');return body}
