export interface EarningsEvent {symbol:string;earningsDate:string;formattedDate:string}
export interface EarningsCalendarResponse {events:EarningsEvent[];requestedSymbols:number;matchedSymbols:number;source:string}
