import type { SectorResearch, SectorSummary } from '../types';

async function request<T>(path:string):Promise<T>{const response=await fetch(path),body=await response.json();if(!response.ok)throw new Error(body.error??'Unable to load market research');return body}
export const getSectors=()=>request<SectorSummary[]>('/api/research/sectors');
export const getSectorResearch=(sector:string)=>request<SectorResearch>(`/api/research/sectors/${sector}`);
