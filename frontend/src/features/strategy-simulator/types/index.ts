import type { OptionType } from '../../options/types';

export interface StrategyLeg {id:string;asset:'option'|'stock';side:'long'|'short';type:OptionType;quantity:number;strike:number;premium:number;dte:number;iv:number}
export interface StrategyTemplate {id:string;name:string;category:'Basic'|'Spreads'|'Advanced'|'Custom';description:string;legs:Array<Partial<StrategyLeg>&{offset?:number}>}
