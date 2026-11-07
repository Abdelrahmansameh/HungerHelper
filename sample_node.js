const fs = require('fs');
const html = fs.readFileSync('quests_tree.html', 'utf8');

const sample = html.match(/<[^>]*\bdata-quest="a-warm-welcome"[\s\S]*?<\/[a-z0-9]+>/i);
if (sample) {
  console.log('Sample node HTML:');
  console.log(sample[0]);
}

const sample2 = html.match(/<[^>]*\bdata-quest="making-dough"[\s\S]*?<\/[a-z0-9]+>/i);
if (sample2) {
  console.log('Sample 2 node HTML:');
  console.log(sample2[0]);
}
