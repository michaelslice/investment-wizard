import { useCallback, useEffect, useState } from 'react';
import { getPriceHistory } from '../api/getPriceHistory';
import type { PriceHistoryResponse } from '../types';

export function usePriceHistory(initialSymbol='AAPL',initialPeriod='1y'){const[data,setData]=useState<PriceHistoryResponse|null>(null),[loading,setLoading]=useState(false),[error,setError]=useState<string|null>(null);const load=useCallback(async(symbol:string,period:string)=>{setLoading(true);setError(null);try{setData(await getPriceHistory(symbol.toUpperCase(),period))}catch(value){setError(value instanceof Error?value.message:'Unable to load price history')}finally{setLoading(false)}},[]);useEffect(()=>{void load(initialSymbol,initialPeriod)},[initialSymbol,initialPeriod,load]);return{data,loading,error,load}}
