import { useEffect, useState } from 'react';
import { getEarningsCalendar } from '../api/getEarningsCalendar';
import type { EarningsCalendarResponse } from '../types';

export function useEarningsCalendar(){const[data,setData]=useState<EarningsCalendarResponse|null>(null),[error,setError]=useState<string|null>(null),[loading,setLoading]=useState(true);useEffect(()=>{getEarningsCalendar().then(setData).catch(value=>setError(value instanceof Error?value.message:'Unable to load earnings calendar')).finally(()=>setLoading(false))},[]);return{data,error,loading}}
