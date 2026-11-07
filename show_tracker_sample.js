const fs = require('fs');
const content = fs.readFileSync('tracker.js', 'utf8');

// Print first 100 lines and lines mentioning fetch or api
const lines = content.split('\n');
console.log('Total lines:', lines.length);
console.log('--- First 60 lines ---');
console.log(lines.slice(0, 60).join('\n'));

console.log('--- Lines mentioning api or fetch ---');
lines.forEach((l, i) => {
  if (l.includes('api') || l.includes('fetch') || l.includes('HUNGER_TRACKER') || l.includes('render')) {
    console.log(`L${i+1}: ${l.trim().slice(0, 160)}`);
  }
});
