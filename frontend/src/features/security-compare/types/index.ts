import type { PriceHistoryResponse } from '../../price-history/types';

export interface ComparisonSeries extends PriceHistoryResponse {
  color: string;
}
