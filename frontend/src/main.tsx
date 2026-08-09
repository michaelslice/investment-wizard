import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { App } from './app/App';
import './styles/global.css';
import './styles/compare.css';
import './styles/thesis.css';
import './styles/view-switcher.css';
import './styles/view-switcher-search.css';
import './styles/focus.css';
import './styles/greek-toast.css';
import './styles/strategy-simulator.css';
import './styles/holders.css';
import './styles/option-chain.css';
import './styles/ticker-stock-chart.css';

createRoot(document.getElementById('root')!).render(<StrictMode><App /></StrictMode>);
