import type { OptionHistoryResponse } from '../types';

export async function getOptionHistory(contractSymbol:string):Promise<OptionHistoryResponse>{const response=await fetch(`/api/options/history/${encodeURIComponent(contractSymbol)}`),body=await response.json();if(!response.ok)throw new Error(body.error??body.detail??'Unable to load contract history');return body}
