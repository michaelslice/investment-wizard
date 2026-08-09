import type { TickerResearchData } from '../types';

export async function getTickerResearch(symbol:string):Promise<TickerResearchData>{const response=await fetch(`/api/research/tickers/${encodeURIComponent(symbol)}`),body=await response.json();if(!response.ok)throw new Error(body.error??body.detail??'Unable to load ticker research');return body}
