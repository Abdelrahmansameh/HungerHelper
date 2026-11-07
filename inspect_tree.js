const fs = require('fs');
const html = fs.readFileSync('quests_tree.html', 'utf8');
console.log('HTML Length:', html.length);

// Look for data- attributes, JSON, script tags, SVG, etc.
const scripts = [];
const scriptRegex = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
let m;
while ((m = scriptRegex.exec(html)) !== null) {
  if (m[2].trim().length > 0) {
    scripts.push({
      len: m[2].length,
      preview: m[2].slice(0, 300).replace(/\s+/g, ' ')
    });
  }
}
console.log('Inline scripts count:', scripts.length);
scripts.forEach((s, idx) => {
  console.log(`Script ${idx} (len ${s.len}): ${s.preview}`);
});

// Check for tree elements / nodes
const dataAttrs = [...html.matchAll(/data-([a-z\-]+)="([^"]+)"/g)].slice(0, 30);
console.log('Sample data attributes:');
dataAttrs.forEach(d => console.log(`${d[1]} = ${d[2].slice(0, 80)}`));
