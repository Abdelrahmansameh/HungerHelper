const fs = require('fs');

async function checkSite() {
  const url = 'https://hunger-companion.com/tracker';
  const res = await fetch(url, {
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
  });
  const html = await res.text();
  console.log('Status:', res.status, 'HTML length:', html.length);
  fs.writeFileSync('page_sample.html', html, 'utf8');

  // Script tags
  const scripts = [];
  const scriptRegex = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
  let match;
  while ((match = scriptRegex.exec(html)) !== null) {
    const attrs = match[1];
    const content = match[2];
    const srcMatch = attrs.match(/src=["']([^"']+)["']/i);
    if (srcMatch) {
      scripts.push({ type: 'src', src: srcMatch[1] });
    } else {
      scripts.push({ type: 'inline', length: content.length, preview: content.slice(0, 200).replace(/\s+/g, ' ') });
    }
  }
  console.log('Scripts found:', JSON.stringify(scripts, null, 2));

  // Check what pages or navigation links exist
  const links = [];
  const linkRegex = /href=["']([^"']+)["']/gi;
  while ((match = linkRegex.exec(html)) !== null) {
    if (!links.includes(match[1])) links.push(match[1]);
  }
  console.log('Links found:', links);
}

checkSite().catch(console.error);
