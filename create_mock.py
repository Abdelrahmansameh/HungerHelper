with open(r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee\eloise_raid_planner.html", "r", encoding="utf-8") as f:
    s = f.read()

# Extract script
p1 = s.find("<script>")
p2 = s.find("</script>")
script = s[p1+8:p2]

with open(r"C:\Users\PC\Documents\HungerHelper\test_run_node.js", "w", encoding="utf-8") as f_out:
    f_out.write("""
const mockElement = (id) => ({
    id,
    classList: { add: () => {}, remove: () => {} },
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

""" + script + """

console.log('Initial tactical-img src len:', elements['tactical-img'] ? elements['tactical-img'].src.length : 'none');
selectRaid(6);
console.log('After selectRaid(6), tactical-img src prefix:', elements['tactical-img'].src.slice(0, 50));
console.log('After selectRaid(6), map-phase-badge text:', elements['map-phase-badge'].textContent);
""")
print("Created test_run_node.js")
