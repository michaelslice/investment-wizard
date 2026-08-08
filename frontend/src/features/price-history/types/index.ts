export interface PricePoint { date:string; open:number; high:number; low:number; close:number; volume:number }
export interface TimelineEarningsEvent { earningsDate:string; epsEstimate:number|null; reportedEps:number|null; surprisePercent:number|null; isUpcoming:boolean }
export interface PriceHistoryResponse { symbol:string; period:string; prices:PricePoint[]; earnings:TimelineEarningsEvent[]; latestPrice:number|null; source:string }
