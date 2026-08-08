export type OptionType = 'call' | 'put';
export type GreekKey = 'delta' | 'gamma' | 'theta' | 'vega' | 'rho';
export interface OptionContract {symbol:string;type:OptionType;strike:number;bid:number;ask:number;last:number;change:number;volume:number;openInterest:number;impliedVolatility:number;inTheMoney:boolean;lastTrade:string|null;previousClose:number|null}
export interface OptionChain {symbol:string;spot:number;spotChange:number;marketTime:number;currency:string;expirations:number[];selectedExpiration:number;calls:OptionContract[];puts:OptionContract[];source:string}
export interface Greeks {delta:number;gamma:number;theta:number;vega:number;rho:number;optionPrice:number}
export interface ProjectionPoint extends Greeks {elapsed:number;remaining:number;spot:number}
