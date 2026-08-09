export type AccountType='brokerage'|'roth-ira'|'401k'|'bank'|'high-yield-savings';
export interface NetWorthAccount {id:string;name:string;institution:string;type:AccountType;balance:number;updatedAt:string}
export interface NetWorthSnapshot {date:string;total:number}
