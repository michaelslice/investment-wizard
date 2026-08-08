import type { EarningsCalendarResponse } from '../types';

export async function getEarningsCalendar():Promise<EarningsCalendarResponse>{const response=await fetch('/api/earnings');const body=await response.json();if(!response.ok)throw new Error(body.error??'Unable to load earnings calendar');return body}
