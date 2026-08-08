import { useEffect, useState } from 'react';
import { getSectorResearch, getSectors } from '../api/getResearch';
import type { SectorResearch, SectorSummary } from '../types';

export function useMarketResearch(){const[sectors,setSectors]=useState<SectorSummary[]>([]),[selected,setSelected]=useState('technology'),[data,setData]=useState<SectorResearch|null>(null),[loading,setLoading]=useState(true),[error,setError]=useState<string|null>(null);useEffect(()=>{getSectors().then(setSectors).catch(value=>setError(value instanceof Error?value.message:'Unable to load sectors'))},[]);useEffect(()=>{setLoading(true);setError(null);getSectorResearch(selected).then(setData).catch(value=>setError(value instanceof Error?value.message:'Unable to load research')).finally(()=>setLoading(false))},[selected]);return{sectors,selected,setSelected,data,loading,error}}
