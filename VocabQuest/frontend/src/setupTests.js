import '@testing-library/jest-dom';

const originalConsoleError = console.error;
const originalConsoleWarn = console.warn;

// Suppress Recharts console errors regarding responsive container dimensions
// which happen in JSDOM environment where elements have 0 dimensions.
console.error = (...args) => {
  if (typeof args[0] === 'string' && args[0].includes('The width(-1) and height(-1)')) {
     return;
  }
  originalConsoleError(...args);
};

console.warn = (...args) => {
    if (typeof args[0] === 'string' && args[0].includes('The width(-1) and height(-1)')) {
        return;
    }
    originalConsoleWarn(...args);
};
