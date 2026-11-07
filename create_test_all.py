with open(r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee\eloise_raid_planner.html", "r", encoding="utf-8") as f:
    s = f.read()

import re
scripts = list(re.finditer(r'<script(?:\s+[^>]*)?>([\s\S]*?)<\/script>', s))
main_script = scripts[1].group(1)

with open(r"C:\Users\PC\Documents\HungerHelper\test_all_raids.js", "w", encoding="utf-8") as f_out:
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

console.log('Testing selectRaid for all indices 0 to 8:');
for (let idx = 0; idx <= 8; idx++) {
    selectRaid(idx);
    console.log(`Index ${idx}: quest='${elements['brief-quest-name'].textContent}', steps=${elements['tactical-steps'].innerHTML.length > 0}, conts=${elements['container-targets'].innerHTML.length > 0}, mobs=${elements['mob-targets'].innerHTML.length > 0}`);
}
""")
print("Created test_all_raids.js")
