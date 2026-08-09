export type TradeStatus='draft'|'planned'|'open'|'closed';

export interface TradeWriteup {
  id:string; createdAt:string; updatedAt:string; title:string; ticker:string; status:TradeStatus;
  direction:string; expectedMove:string; timeHorizon:string; catalyst:string; edge:string;
  invalidation:string; whyOptions:string; setup:string; entryCriteria:string;
  optionStructure:string; expiration:string; dte:string; strike:string; delta:string; iv:string;
  portfolioSize:string; riskPercent:string; premium:string; totalExposureLimit:string;
  profitExit:string; lossExit:string; timeExit:string; rules:string;
  resultPercent:string; resultMoney:string; ruleFollowed:string; review:string;
}
