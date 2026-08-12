import type{OptionContract}from '../../options/types';
export interface EyeResult{underlying:string;spot:number;expiration:number;dte:number;moneyness:number;spreadPercent:number;contract:OptionContract&{publishedGreeks:{delta:number|null;gamma:number|null;theta:number|null;vega:number|null;rho:number|null}}}
export interface EyeResponse{results:EyeResult[];contractsScanned:number;symbolsScanned:number;source:string}
export interface EyeFilters{symbols:string;option_type:string;min_dte:string;max_dte:string;min_moneyness:string;max_moneyness:string;min_price:string;max_price:string;min_iv:string;max_iv:string;min_delta:string;max_delta:string;min_volume:string;min_open_interest:string;max_spread_percent:string}
