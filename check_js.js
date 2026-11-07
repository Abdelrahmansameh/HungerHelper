const fs = require('fs');

for (const f of ['tracker.js', 'progress-core.js', 'progress-sync.js', 'item-card.js']) {
  if (fs.existsSync(f)) {
    const content = fs.readFileSync(f, 'utf8');
    console.log(`=== ${f} (${content.length} bytes) ===`);
    // Find fetch or api urls
    const fetchMatches = [...content.matchAll(/fetch\s*\(\s*[`"']([^`"']+)`|["']/g)].map(m => m[1]);
    console.log('Fetches:', [...new Set(fetchMatches)]);
    const apiMatches = [...content.matchAll(/\/api\/[a-zA-Z0-9_\-\/]+/g)].map(m => m[0]);
    console.log('API paths:', [...new Set(apiMatches)]);
    const locStorage = [...content.matchAll(/localStorage\.[a-zA-Z0-9_]+/g)].map(m => m[0]);
    console.log('LocalStorage calls:', [...new Set(locStorage)]);
    const storageKeys = [...content.matchAll(/localStorage\.(?:getItem|setItem|removeItem)\s*\(\s*['"]([^'"]+)['"]/g)].map(m => m[1]);
    console.log('Storage keys:', [...new Set(storageKeys)]);
  }
}
