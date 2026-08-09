import type { EarningsCalendarResponse } from '../types';

export async function getEarningsCalendar(symbols?:string[]):Promise<EarningsCalendarResponse>{const query=symbols?.length?`?symbols=${encodeURIComponent(symbols.join(','))}`:'',response=await fetch(`/api/earnings${query}`),body=await response.json();if(!response.ok)throw new Error(body.error??'Unable to load earnings calendar');return body}
