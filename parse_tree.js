const fs = require('fs');
const html = fs.readFileSync('quests_tree.html', 'utf8');

// Find all elements with data-quest
const matches = [...html.matchAll(/<([a-z0-9]+)[^>]*\bdata-quest="([^"]+)"[^>]*>([\s\S]*?)<\/\1>/gi)];
console.log('Matches count with data-quest:', matches.length);

const questTreeList = [];
const itemRegex = /<[^>]*\bdata-quest="([^"]+)"([^>]*)>([\s\S]*?)<\/[a-z0-9]+>/gi;
let m;
while ((m = itemRegex.exec(html)) !== null) {
  const slug = m[1];
  const attrs = m[2];
  const body = m[3];
  const afterMatch = attrs.match(/data-after="([^"]+)"/);
  const findMatch = attrs.match(/data-find="([^"]+)"/);
  const hrefMatch = body.match(/href="([^"]+)"/);
  const titleMatch = body.match(/class="[^"]*qt-title[^"]*"[^>]*>([^<]+)</i) || body.match(/<span[^>]*>([^<]+)<\/span>/i);
  questTreeList.push({
    slug,
    after: afterMatch ? afterMatch[1] : null,
    find: findMatch ? findMatch[1] : null,
    href: hrefMatch ? hrefMatch[1] : null,
    title: titleMatch ? titleMatch[1].trim() : slug
  });
}

console.log('Parsed quests count:', questTreeList.length);
console.log('First 15 quests in tree:');
console.log(JSON.stringify(questTreeList.slice(0, 15), null, 2));

fs.writeFileSync('tree_quests_parsed.json', JSON.stringify(questTreeList, null, 2));
