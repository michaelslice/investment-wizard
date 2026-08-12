export type SandboxViewKey='options'|'chain'|'eye'|'simulator'|'earnings'|'earnings-history'|'price-history'|'daily-performance'|'compare'|'research'|'watchlist'|'focus'|'holders'|'real-estate'|'net-worth'|'journal'|'chat';
export interface SandboxPanel{id:string;view:SandboxViewKey;title:string;x:number;y:number;width:number;height:number;z:number}
