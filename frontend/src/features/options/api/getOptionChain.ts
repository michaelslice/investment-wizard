import type { OptionChain } from '../types';

export async function getOptionChain(symbol:string, expiration?:number):Promise<OptionChain>{
  const query=new URLSearchParams({symbol});if(expiration)query.set('expiration',String(expiration));
  const response=await fetch(`/api/options?${query}`);const body=await response.json();
  if(!response.ok)throw new Error(body.error??'Unable to load option chain');return body;
}
