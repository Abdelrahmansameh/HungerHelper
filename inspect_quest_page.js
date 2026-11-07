const fs = require('fs');
const html = fs.readFileSync('quest_sample.html', 'utf8');

// Title and heading
const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
console.log('Title:', titleMatch ? titleMatch[1] : '');

// Look for quest fiche / main content
// Let's strip scripts and inspect text structure
const mainMatch = html.match(/<main\b[^>]*>([\s\S]*?)<\/main>/i);
if (mainMatch) {
  const main = mainMatch[1];
  console.log('Main length:', main.length);
  // Look for sections or headings
  const headings = [...main.matchAll(/<h[1-4][^>]*>([\s\S]*?)<\/h[1-4]>/gi)].map(m => m[1].replace(/<[^>]+>/g, '').trim());
  console.log('Headings:', headings);

  // Look for objectives
  const objMatches = [...main.matchAll(/<li[^>]*class="[^"]*obj[^"]*"[^>]*>([\s\S]*?)<\/li>/gi)].map(m => m[1].replace(/<[^>]+>/g, ' ').trim());
  console.log('Objectives (class obj):', objMatches);

  // Look for data-obj or checkboxes
  const objIds = [...main.matchAll(/data-obj(?:-id)?="([^"]+)"/gi)].map(m => m[1]);
  console.log('Obj IDs:', objIds);

  // Look for maps mentioned
  const mapLinks = [...main.matchAll(/href="(\/maps\/[^"]+)"/gi)].map(m => m[1]);
  console.log('Map links:', [...new Set(mapLinks)]);

  // Look for items mentioned
  const itemLinks = [...main.matchAll(/href="(\/items\/[^"]+)"/gi)].map(m => m[1]);
  console.log('Item links:', [...new Set(itemLinks)]);
}
