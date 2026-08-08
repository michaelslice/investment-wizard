import type { PriceHistoryResponse } from '../types';

export async function getPriceHistory(symbol:string,period:string):Promise<PriceHistoryResponse>{const response=await fetch(`/api/prices/${encodeURIComponent(symbol)}?period=${period}`),body=await response.json();if(!response.ok)throw new Error(body.error??body.detail??'Unable to load price history');return body}
