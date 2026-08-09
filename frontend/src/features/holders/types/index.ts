export interface InstitutionalHolder {name:string;shares:number;value:number|null;percentHeld:number|null;changePercent:number|null;reportedDate:string|null}
export interface HoldersResponse {symbol:string;holders:InstitutionalHolder[];source:string}
export interface HolderRect {holder:InstitutionalHolder;x:number;y:number;width:number;height:number}
