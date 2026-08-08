import { useCallback, useEffect, useState } from 'react';
import { getOptionChain } from '../api/getOptionChain';
import type { OptionChain } from '../types';

export function useOptionChain(initialSymbol='AAPL'){
  const [data,setData]=useState<OptionChain|null>(null);const [loading,setLoading]=useState(false);const [error,setError]=useState<string|null>(null);
  const load=useCallback(async(symbol:string,expiration?:number)=>{setLoading(true);setError(null);try{setData(await getOptionChain(symbol.toUpperCase(),expiration))}catch(value){setError(value instanceof Error?value.message:'Unable to load option chain')}finally{setLoading(false)}},[]);
  useEffect(()=>{void load(initialSymbol)},[initialSymbol,load]);return{data,loading,error,load};
}
