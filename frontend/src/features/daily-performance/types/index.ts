export interface DailySession{date:string;open:number;high:number;low:number;close:number;volume:number;closeReturn:number|null;gap:number|null;intradayReturn:number;upsideExcursion:number;downsideExcursion:number;range:number;weekday:string}
export interface IntradayPoint{timestamp:string;open:number;high:number;low:number;close:number;volume:number}
export interface IntradaySessionResponse{symbol:string;sessionDate:string;interval:string;points:IntradayPoint[];source:string}
