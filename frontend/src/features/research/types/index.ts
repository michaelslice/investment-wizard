export interface SectorSummary {slug:string;label:string;companyCount:number}
export interface CompanyResearch {symbol:string;name:string;sector:string;industry:string;marketCap:number|null;currentPrice:number|null;trailingPe:number|null;revenue:number|null;profitMargin:number|null;targetPrice:number|null;recommendation:string|null}
export interface SectorResearch {sector:SectorSummary;companies:CompanyResearch[];totalCount:number;page:number;pageSize:number;source:string}
