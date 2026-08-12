import { useEffect, useState } from 'react';

export const APPLICATION_VIEWS=[
  {id:'options',label:'Options terminal'},
  {id:'chain',label:'Options chain'},
  {id:'eye',label:'The Eye'},
  {id:'simulator',label:'Strategy lab'},
  {id:'earnings',label:'Upcoming earnings'},
  {id:'earnings-history',label:'Earnings reactions'},
  {id:'price-history',label:'Price history'},
  {id:'daily-performance',label:'1-day evaluator'},
  {id:'compare',label:'Compare'},
  {id:'research',label:'Market research'},
  {id:'watchlist',label:'Watchlist'},
  {id:'focus',label:'Focus'},
  {id:'holders',label:'Holders'},
  {id:'net-worth',label:'Net worth'},
  {id:'kelly',label:'Kelly lab'},
  {id:'real-estate',label:'Real estate'},
  {id:'sandbox',label:'Sandbox'},
  {id:'journal',label:'Trade journal'},
  {id:'chat',label:'AI research'},
] as const;

export type ViewId=typeof APPLICATION_VIEWS[number]['id'];
const STORAGE_KEY='investment-wizard.enabled-views.v1',SANDBOX_MIGRATION_KEY='investment-wizard.enabled-views.sandbox-migrated',DAILY_MIGRATION_KEY='investment-wizard.enabled-views.daily-performance-migrated',EVENT='investment-wizard:view-preferences';
const allViews=()=>APPLICATION_VIEWS.map(view=>view.id);

export function readEnabledViews():ViewId[]{try{const parsed=JSON.parse(localStorage.getItem(STORAGE_KEY)??'null');if(Array.isArray(parsed)){const valid=parsed.filter((id):id is ViewId=>APPLICATION_VIEWS.some(view=>view.id===id));if(!localStorage.getItem(SANDBOX_MIGRATION_KEY)){localStorage.setItem(SANDBOX_MIGRATION_KEY,'1');if(!valid.includes('sandbox'))valid.push('sandbox')}if(!localStorage.getItem(DAILY_MIGRATION_KEY)){localStorage.setItem(DAILY_MIGRATION_KEY,'1');if(!valid.includes('daily-performance'))valid.push('daily-performance')}return valid.length?valid:allViews()}}catch{/* Restore defaults when browser data is malformed. */}return allViews()}
export function saveEnabledViews(ids:ViewId[]){localStorage.setItem(STORAGE_KEY,JSON.stringify(ids));window.dispatchEvent(new CustomEvent(EVENT))}
export function useEnabledViews(){const[enabled,setEnabled]=useState<ViewId[]>(readEnabledViews);useEffect(()=>{const update=()=>setEnabled(readEnabledViews());window.addEventListener(EVENT,update);window.addEventListener('storage',update);return()=>{window.removeEventListener(EVENT,update);window.removeEventListener('storage',update)}},[]);return enabled}
