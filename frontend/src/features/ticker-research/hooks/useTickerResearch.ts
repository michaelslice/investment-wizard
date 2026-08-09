import { useEffect, useState } from 'react';
import { getTickerResearch } from '../api/getTickerResearch';
import type { TickerResearchData } from '../types';

export function useTickerResearch(symbol:string){const[data,setData]=useState<TickerResearchData|null>(null),[loading,setLoading]=useState(true),[error,setError]=useState<string|null>(null);useEffect(()=>{setLoading(true);setData(null);setError(null);getTickerResearch(symbol).then(setData).catch(value=>setError(value instanceof Error?value.message:'Unable to load ticker research')).finally(()=>setLoading(false))},[symbol]);return{data,loading,error}}
