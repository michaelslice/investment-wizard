import { useCallback, useEffect, useState } from 'react';
import { getEarningsHistory } from '../api/getEarningsHistory';
import type { EarningsHistoryResponse } from '../types';

export function useEarningsHistory(initial='AAPL'){const[data,setData]=useState<EarningsHistoryResponse|null>(null),[loading,setLoading]=useState(false),[error,setError]=useState<string|null>(null);const load=useCallback(async(symbol:string)=>{setLoading(true);setError(null);try{setData(await getEarningsHistory(symbol.toUpperCase()))}catch(value){setError(value instanceof Error?value.message:'Unable to load historical earnings')}finally{setLoading(false)}},[]);useEffect(()=>{void load(initial)},[initial,load]);return{data,loading,error,load}}
