import type {PropertyFilters,PropertySearchResponse} from '../types';

export async function searchProperties(filters:PropertyFilters,offset=0):Promise<PropertySearchResponse>{const params=new URLSearchParams({limit:'25',offset:String(offset)});Object.entries(filters).forEach(([key,value])=>{if(value.trim())params.set(key,value.trim())});const response=await fetch(`/api/real-estate/listings?${params}`);const body=await response.json();if(!response.ok)throw new Error(body.detail??body.error??'Unable to search real-estate listings');return body}
