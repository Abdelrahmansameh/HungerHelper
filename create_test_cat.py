with open(r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee\eloise_raid_planner.html", "r", encoding="utf-8") as f:
    s = f.read()

import re
scripts = list(re.finditer(r'<script(?:\s+[^>]*)?>([\s\S]*?)<\/script>', s))
main_script = scripts[1].group(1)

with open(r"C:\Users\PC\Documents\HungerHelper\test_categories_node.js", "w", encoding="utf-8") as f_out:
    f_out.write("""
const mockElement = (id) => ({
    id,
    classList: { 
        classes: new Set(),
        add: function(c) { this.classes.add(c); },
        remove: function(c) { this.classes.delete(c); },
        contains: function(c) { return this.classes.has(c); }
    },
    innerHTML: '',
    textContent: '',
    className: '',
    src: '',
    style: {}
});
const elements = {};
global.document = {
    getElementById: (id) => {
        if (!elements[id]) elements[id] = mockElement(id);
        return elements[id];
    },
    addEventListener: () => {}
};
global.localStorage = {
    getItem: () => null,
    setItem: () => {}
};

""" + main_script + """

console.log('Testing categories for Raid 1:');
selectRaid(1);
console.log('tactical-steps length:', elements['tactical-steps'].innerHTML.length);
console.log('container-targets length:', elements['container-targets'].innerHTML.length);
console.log('mob-targets length:', elements['mob-targets'].innerHTML.length);
console.log('stash-checklist length:', elements['stash-checklist'].innerHTML.length);
console.log('Sample tactical-steps:', elements['tactical-steps'].innerHTML.slice(0, 100));
console.log('Sample container-targets:', elements['container-targets'].innerHTML.slice(0, 100));
console.log('Sample stash-checklist:', elements['stash-checklist'].innerHTML.slice(0, 100));
""")
print("Created test_categories_node.js")
