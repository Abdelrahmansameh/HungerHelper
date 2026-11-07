const fs = require('fs');
const urls = JSON.parse(fs.readFileSync('en_urls.json', 'utf8'));

const questUrls = urls.filter(u => u.includes('/quests/'));
console.log('Quest URLs count:', questUrls.length);
console.log('Sample quest URLs:', questUrls.slice(0, 30));

const mapUrls = urls.filter(u => u.includes('/maps'));
console.log('Map URLs:', mapUrls);

const npcUrls = urls.filter(u => u.includes('/npcs'));
console.log('NPC URLs count:', npcUrls.length, npcUrls.slice(0, 10));

const toKeep = urls.filter(u => u.includes('keep') || u.includes('loot') || u.includes('container'));
console.log('Keep / Loot / Container counts:', toKeep.length);
