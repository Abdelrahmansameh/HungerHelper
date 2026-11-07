const fs = require('fs');
const html = fs.readFileSync('quests_chrome.html', 'utf8');
console.log('HTML Length:', html.length);
const title = html.match(/<title[^>]*>([^<]+)<\/title>/i);
console.log('Title:', title ? title[1] : 'No title');

// Check for links with /quests/
const questLinks = [...html.matchAll(/href="(\/quests\/[^"]+)"/g)].map(m => m[1]);
console.log('Quest links count:', questLinks.length);
console.log('Sample quest links:', [...new Set(questLinks)].slice(0, 20));

// Check for JSON or script data
const scripts = [...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)].map(m => ({
  attrs: m[1],
  preview: m[2].slice(0, 150).replace(/\s+/g, ' ')
}));
console.log('Scripts:', JSON.stringify(scripts, null, 2));
