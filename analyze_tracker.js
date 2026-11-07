const fs = require('fs');
const html = fs.readFileSync('tracker_chrome.html', 'utf8');
console.log('HTML Length:', html.length);
const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
console.log('Title:', titleMatch ? titleMatch[1] : 'No title');

const scripts = [];
const scriptRegex = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
let m;
while ((m = scriptRegex.exec(html)) !== null) {
  const attrs = m[1];
  const body = m[2];
  const src = (attrs.match(/src=["']([^"']+)["']/i) || [])[1];
  scripts.push({
    src: src || null,
    bodyLen: body.length,
    preview: body.slice(0, 160).replace(/\s+/g, ' ')
  });
}
console.log('Scripts:', JSON.stringify(scripts, null, 2));

// Check for links or buttons or text in body
const bodyText = html.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
                     .replace(/<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>/gi, '')
                     .replace(/<[^>]+>/g, ' ')
                     .replace(/\s+/g, ' ')
                     .trim();
console.log('Body Text sample:', bodyText.slice(0, 500));
