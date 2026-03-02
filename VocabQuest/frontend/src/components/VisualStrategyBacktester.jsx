import React from 'react';

const strategies = [
  { name: 'Master', description: 'No explanation available.' },
  { name: 'Turtle', description: 'Trend Following Strategy: Buying breakouts of 20-day highs. Profiting from strong trends.' },
  { name: 'Isa', description: 'No explanation available.' },
  { name: 'Market', description: 'No explanation available.' },
  { name: 'Ema', description: 'No explanation available.' },
  { name: 'Darvas', description: 'No explanation available.' },
  { name: 'Mms', description: 'No explanation available.' },
  { name: 'Bull Put', description: 'Bullish Strategy: You want the stock to stay ABOVE your short strike. You profit from time decay (Theta).' },
  { name: 'Hybrid', description: 'No explanation available.' },
  { name: 'Fortress', description: 'No explanation available.' },
  { name: 'Quantum', description: 'No explanation available.' },
  { name: 'Alpha101', description: 'No explanation available.' },
  { name: 'Liquidity Grab', description: 'No explanation available.' },
  { name: 'Rsi Divergence', description: 'No explanation available.' },
  { name: 'Martin Luk', description: 'Systematic strategy focused on liquid macro asset classes.' },
  { name: 'Medallion Strategy', description: 'High-frequency quantitative trading strategy.' },
];

const VisualStrategyBacktester = () => {
  return (
    <div className="min-h-screen bg-gray-900 text-gray-300 font-sans">
      {/* Header */}
      <header className="bg-gray-900 border-b border-gray-800 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-8">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-black border border-gray-700 rounded flex items-center justify-center">
              <div className="w-4 h-4 bg-blue-600 rounded-sm"></div>
            </div>
            <span className="text-blue-500 font-bold text-xl tracking-tight">TRADE<span className="text-white">GUARDIAN</span></span>
          </div>

          <div className="flex items-center gap-2">
            <button className="px-3 py-1.5 bg-gray-800 text-xs font-medium rounded border border-gray-700 hover:bg-gray-700 transition-colors">Login</button>
            <button className="px-3 py-1.5 bg-blue-600 text-white text-xs font-medium rounded hover:bg-blue-700 transition-colors flex items-center gap-1">
              <span>+</span> Quick Trade
            </button>
            <button className="px-3 py-1.5 bg-gray-800 text-xs font-medium rounded border border-gray-700 hover:bg-gray-700 transition-colors flex items-center gap-1">
              <span>☑</span> Pre-Flight
            </button>
            <button className="text-gray-400 hover:text-white">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            </button>
          </div>
        </div>

        <nav className="flex items-center gap-6 text-sm font-medium">
          <a href="#" className="hover:text-white transition-colors">Home</a>
          <a href="#" className="hover:text-white transition-colors">Dashboard</a>
          <a href="#" className="hover:text-white transition-colors">Screener</a>
          <a href="#" className="hover:text-white transition-colors">Strategy Guide</a>
          <a href="#" className="text-blue-400 border-b-2 border-blue-500 pb-5 -mb-5">Backtest</a>
          <a href="#" className="hover:text-white transition-colors">Journal</a>
          <a href="#" className="hover:text-white transition-colors">Audit</a>
          <a href="#" className="hover:text-white transition-colors">Risk Map</a>
          <a href="#" className="hover:text-white transition-colors">Monte Carlo</a>
          <a href="#" className="hover:text-white transition-colors">AI Consultant</a>
        </nav>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8 max-w-7xl">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-white mb-2">Visual Strategy Backtester</h1>
          <p className="text-gray-400 text-sm mb-6">Validate your edge before risking capital. Step 1 of 3.</p>

          {/* Progress Bar */}
          <div className="w-full bg-gray-800 rounded-full h-2 mb-8">
            <div className="bg-blue-600 h-2 rounded-full" style={{ width: '33%' }}></div>
          </div>
        </div>

        <h2 className="text-lg font-semibold text-white mb-4">Select a Strategy</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
          {strategies.map((strategy, index) => (
            <div
              key={index}
              className={`bg-gray-800/50 p-5 rounded-lg border cursor-pointer hover:bg-gray-800 transition-all ${index === 0 ? 'border-blue-500 ring-1 ring-blue-500/50' : 'border-gray-700 hover:border-gray-600'}`}
            >
              <h3 className="font-bold text-white text-sm mb-2">{strategy.name}</h3>
              <p className="text-xs text-gray-400 leading-relaxed">{strategy.description}</p>
            </div>
          ))}
        </div>

        <div className="flex justify-end">
          <button className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold rounded transition-colors flex items-center gap-2">
            Next Step <span>→</span>
          </button>
        </div>
      </main>
    </div>
  );
};

export default VisualStrategyBacktester;
