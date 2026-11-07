with open(r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee\eloise_raid_planner.html", "r", encoding="utf-8") as f:
    s = f.read()

import re
scripts = list(re.finditer(r'<script(?:\s+[^>]*)?>([\s\S]*?)<\/script>', s))
main_script = scripts[1].group(1)

with open(r"C:\Users\PC\Documents\HungerHelper\test_run_node_v6.js", "w", encoding="utf-8") as f_out:
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

console.log('Testing selectRaid for all 7 raids:');
for (let raid = 1; raid <= 7; raid++) {
    selectRaid(raid);
    const activeMap = elements[`map-img-${raid}`];
    const isHidden = activeMap.classList.contains('hidden');
    console.log(`Raid ${raid}: map-img-${raid} hidden=${isHidden}, quest=${elements['brief-quest-name'].textContent}`);
}
""")
print("Created test_run_node_v6.js")
