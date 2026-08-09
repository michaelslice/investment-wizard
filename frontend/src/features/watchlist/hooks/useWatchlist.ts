import { useCallback, useEffect, useState } from 'react';
import { getWatchlistCompanies } from '../api/getWatchlistCompanies';
import type { WatchlistCompany } from '../types';

const STORAGE_KEY='investment-wizard.watchlist.v1',LEGACY_STORAGE_KEY='optionscope.watchlist.v1';
const readSymbols=():string[]=>{try{const value=JSON.parse(localStorage.getItem(STORAGE_KEY)??localStorage.getItem(LEGACY_STORAGE_KEY)??'[]');return Array.isArray(value)?value.filter(item=>typeof item==='string'):[]}catch{return[]}};

export function useWatchlist(){const[symbols,setSymbols]=useState<string[]>(readSymbols),[companies,setCompanies]=useState<WatchlistCompany[]>([]),[loading,setLoading]=useState(false),[error,setError]=useState<string|null>(null);useEffect(()=>{localStorage.setItem(STORAGE_KEY,JSON.stringify(symbols));setLoading(Boolean(symbols.length));setError(null);getWatchlistCompanies(symbols).then(setCompanies).catch(value=>setError(value instanceof Error?value.message:'Unable to load watchlist')).finally(()=>setLoading(false))},[symbols]);const add=useCallback((value:string)=>{const symbol=value.trim().toUpperCase();if(symbol)setSymbols(current=>current.includes(symbol)||current.length>=50?current:[...current,symbol])},[]),remove=useCallback((symbol:string)=>setSymbols(current=>current.filter(item=>item!==symbol)),[]);return{symbols,companies,loading,error,add,remove}}
