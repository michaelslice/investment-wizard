import type { WatchlistCompany } from '../types';

export async function getWatchlistCompanies(symbols:string[]):Promise<WatchlistCompany[]>{if(!symbols.length)return[];const response=await fetch(`/api/research/companies?symbols=${encodeURIComponent(symbols.join(','))}`),body=await response.json();if(!response.ok)throw new Error(body.error??body.detail??'Unable to load watchlist');return body}
