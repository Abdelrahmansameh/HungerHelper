const fs = require('fs');
const html = fs.readFileSync('quests_tree.html', 'utf8');

const idx = html.indexOf('data-quest="making-dough"');
console.log(html.slice(idx - 50, idx + 400));
