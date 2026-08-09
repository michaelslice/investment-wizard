import type { StrategyTemplate } from '../types';

const o=(side:'long'|'short',type:'call'|'put',offset=0,quantity=1,dte?:number)=>({asset:'option' as const,side,type,offset,quantity,dte});
const s=(side:'long'|'short',quantity=100)=>({asset:'stock' as const,side,type:'call' as const,quantity,offset:0});
export const STRATEGIES:StrategyTemplate[]=[
  {id:'long-call',name:'Long Call',category:'Basic',description:'Bullish defined-risk call purchase.',legs:[o('long','call',0)]},
  {id:'long-put',name:'Long Put',category:'Basic',description:'Bearish defined-risk put purchase.',legs:[o('long','put',0)]},
  {id:'covered-call',name:'Covered Call',category:'Basic',description:'Long shares financed by a short call.',legs:[s('long'),o('short','call',.08)]},
  {id:'cash-secured-put',name:'Cash Secured Put',category:'Basic',description:'Short put backed by strike-value cash.',legs:[o('short','put',-.08)]},
  {id:'naked-call',name:'Naked Call',category:'Basic',description:'Uncovered bearish short call.',legs:[o('short','call',.08)]},
  {id:'naked-put',name:'Naked Put',category:'Basic',description:'Uncovered bullish short put.',legs:[o('short','put',-.08)]},
  {id:'credit-spread',name:'Credit Spread',category:'Spreads',description:'Bullish put credit spread.',legs:[o('short','put',-.05),o('long','put',-.12)]},
  {id:'call-spread',name:'Call Spread',category:'Spreads',description:'Bull call debit spread.',legs:[o('long','call',-.02),o('short','call',.08)]},
  {id:'put-spread',name:'Put Spread',category:'Spreads',description:'Bear put debit spread.',legs:[o('long','put',.02),o('short','put',-.08)]},
  {id:'poor-mans-covered-call',name:"Poor Man's Covered Call",category:'Spreads',description:'Long-dated deep ITM call against a shorter call.',legs:[o('long','call',-.2,1,180),o('short','call',.08,1,30)]},
  {id:'calendar-spread',name:'Calendar Spread',category:'Spreads',description:'Same strike with long back-month and short front-month options.',legs:[o('long','call',0,1,90),o('short','call',0,1,30)]},
  {id:'ratio-backspread',name:'Ratio Back Spread',category:'Spreads',description:'One short call against two higher-strike long calls.',legs:[o('short','call',0),o('long','call',.1,2)]},
  {id:'iron-condor',name:'Iron Condor',category:'Advanced',description:'Defined-risk short-volatility four-leg range trade.',legs:[o('long','put',-.15),o('short','put',-.08),o('short','call',.08),o('long','call',.15)]},
  {id:'butterfly',name:'Butterfly',category:'Advanced',description:'Three-strike limited-risk target-price trade.',legs:[o('long','call',-.1),o('short','call',0,2),o('long','call',.1)]},
  {id:'collar',name:'Collar',category:'Advanced',description:'Long stock protected by a put and financed by a call.',legs:[s('long'),o('long','put',-.08),o('short','call',.08)]},
  {id:'diagonal-spread',name:'Diagonal Spread',category:'Advanced',description:'Different strikes and expirations.',legs:[o('long','call',-.1,1,120),o('short','call',.08,1,30)]},
  {id:'double-diagonal',name:'Double Diagonal',category:'Advanced',description:'Put and call diagonals combined.',legs:[o('long','put',-.15,1,120),o('short','put',-.08,1,30),o('short','call',.08,1,30),o('long','call',.15,1,120)]},
  {id:'straddle',name:'Straddle',category:'Advanced',description:'Long call and put at the same strike.',legs:[o('long','call',0),o('long','put',0)]},
  {id:'strangle',name:'Strangle',category:'Advanced',description:'Long OTM put and call.',legs:[o('long','put',-.08),o('long','call',.08)]},
  {id:'covered-strangle',name:'Covered Strangle',category:'Advanced',description:'Long shares with short OTM call and put.',legs:[s('long'),o('short','put',-.08),o('short','call',.08)]},
  {id:'synthetic-put',name:'Synthetic Put',category:'Advanced',description:'Long shares combined with a protective put.',legs:[s('long'),o('long','put',0)]},
  {id:'reverse-conversion',name:'Reverse Conversion',category:'Advanced',description:'Short shares, long call, and short put at one strike.',legs:[s('short'),o('long','call',0),o('short','put',0)]},
  ...[2,3,4,5,6,8].map(count=>({id:`custom-${count}`,name:`Custom ${count} Legs`,category:'Custom' as const,description:`Build a custom ${count}-leg options position.`,legs:Array.from({length:count},(_,index)=>o(index%2?'short':'long',index%2?'put':'call',(index-(count-1)/2)*.05))})),
];
