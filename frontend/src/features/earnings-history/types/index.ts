export interface EarningsReaction {reportDate:string;timing:string;beforeSessionDate:string;beforeClose:number;nextSessionDate:string;nextOpen:number;change:number;changePercent:number;profitOn100Shares:number;epsEstimate:number|null;reportedEps:number|null;surprisePercent:number|null}
export interface EarningsHistoryResponse {symbol:string;events:EarningsReaction[];averageChangePercent:number;positiveReactions:number;source:string}
export interface EarningsPricePoint {timestamp:string;open:number;high:number;low:number;close:number;volume:number}
export interface EarningsReactionChartResponse {symbol:string;beforeSessionDate:string;nextSessionDate:string;points:EarningsPricePoint[];tradingDays:number;interval:string;source:string}
