import json
import base64
import os
import subprocess
from PIL import Image

# Load talent data
with open('user_talents_summary.json', 'r', encoding='utf-8') as f:
    trees = json.load(f)

# Flatten talents with tree slug & color info
all_talents = {}
for tree in trees:
    for t in tree['talents']:
        t['tree_slug'] = tree['slug']
        t['tree_name'] = tree['name']
        all_talents[t['name']] = t

# Base64 icons
icons_b64 = {}
for root, dirs, files in os.walk('talent_icons'):
    for file in files:
        if file.endswith('.png'):
            with open(os.path.join(root, file), 'rb') as img_f:
                icons_b64[file] = "data:image/png;base64," + base64.b64encode(img_f.read()).decode('ascii')

ROMAN = ["0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]

# Functional groupings requested by user:
# 1. STAMINA & MOVEMENT
# 2. ENERGY & MELEE ATTACK
# 3. DEFENSE, ARMOR & HEALING
# 4. RADAR, RECON & UTILITY

categories = [
    {
        "id": "stamina_movement",
        "title": "STAMINA & MOVEMENT",
        "icon": "🏃",
        "accent": "#38bdf8",     # Cyan / Sky
        "accent_bg": "rgba(56, 189, 248, 0.12)",
        "accent_border": "rgba(56, 189, 248, 0.35)",
        "summary": [
            ("Max Move Speed", "+31% (Hugo) / +29% (Gabriel)"),
            ("2H Lunge Velocity", "+25% Attack Dash (Fencing)"),
            ("Sprint Stamina Drain", "-30% Drain (Endurance)"),
            ("Stamina Recovery Delay", "100% Sooner / 0s Delay"),
            ("Jump & Vault Cost", "-40% Stamina (Leap)"),
            ("Stamina Recovery Rate", "+30% Faster (Oxygenation)")
        ],
        "talents": [
            {"name": "Endurance", "highlight": "-30% Sprint Stamina Drain"},
            {"name": "Catching Breath", "highlight": "Stamina Recovery Delay: 0s (Instant)"},
            {"name": "Leap", "highlight": "-40% Jump & Vault Stamina Cost"},
            {"name": "Oxygenation", "highlight": "+30% Faster Stamina Recovery Rate"},
            {"name": "Overlander", "highlight": "+8% Movespeed with 2H Drawn"},
            {"name": "Shock", "highlight": "+15% Movespeed for 20s when Damaged"},
            {"name": "Fencing", "highlight": "Melee Attacks Gain Forward Lunge"},
            {"name": "Advanced Footwork", "highlight": "+25% Lunge Speed for 2H Weapons"},
            {"name": "Limber", "highlight": "+16% Lunge Speed for 1H Weapons"}
        ]
    },
    {
        "id": "energy_melee",
        "title": "ENERGY & MELEE COMBAT",
        "icon": "⚔️",
        "accent": "#e5c07b",     # Gold
        "accent_bg": "rgba(229, 192, 123, 0.12)",
        "accent_border": "rgba(229, 192, 123, 0.4)",
        "summary": [
            ("2H Light Attack Cost", "-25% Energy (Deft Strikes)"),
            ("2H Heavy Attack Cost", "-25% Energy (Expert Strikes)"),
            ("Sprint Melee Attack Cost", "-25% Energy (Blitz)"),
            ("Energy Regen Delay", "50% Faster Start (Phalanx)"),
            ("Energy Regen Rate", "+25% Faster (Guard Recovery)"),
            ("Kill / Down Momentum", "+20 Energy Restored (Relentless)")
        ],
        "talents": [
            {"name": "Deft Strikes", "highlight": "-25% Light Attack Energy (2H)"},
            {"name": "Expert Strikes", "highlight": "-25% Heavy Attack Energy (2H)"},
            {"name": "Blitz", "highlight": "-25% Sprint Attack Energy Cost"},
            {"name": "Phalanx", "highlight": "Energy Regen Starts 50% Faster"},
            {"name": "Guard Recovery", "highlight": "+25% Faster Energy Regen Rate"},
            {"name": "Relentless", "highlight": "+20 Energy on Enemy Down / Kill"}
        ]
    },
    {
        "id": "defense_sustain",
        "title": "DEFENSE & HEALING SUSTAIN",
        "icon": "🛡️",
        "accent": "#4ade80",     # Emerald
        "accent_bg": "rgba(74, 222, 128, 0.12)",
        "accent_border": "rgba(74, 222, 128, 0.35)",
        "summary": [
            ("Ranged Projectile DR", "-20% DR (Berzerker Keystone)"),
            ("Leg Armor Slot", "Unlocked (Full 3-Piece Coverage)"),
            ("Armor Repair Heal", "Heals 50% of Repaired Armor"),
            ("Armor Repair Speed", "+50% Faster Tool Use (Fastening)"),
            ("Medical Item Healing", "+18% Bonus HP (Operation)"),
            ("Downed Teammate Revive", "+30% Faster Revive Speed (Surgeon)")
        ],
        "talents": [
            {"name": "Berzerker", "highlight": "★ KEYSTONE: -20% Projectile Dmg Taken"},
            {"name": "Leg Armour", "highlight": "Equip Leg Armour Unlocked (Full 3-Pc)"},
            {"name": "Toughen Up", "highlight": "★ KEYSTONE: Heal 50% of Repaired Armor"},
            {"name": "Fastening", "highlight": "+50% Faster Armor Repair Tool Speed"},
            {"name": "Operation", "highlight": "+18% Bonus Healing from Medicines"},
            {"name": "Surgeon", "highlight": "+30% Faster Teammate Revive Speed"}
        ]
    },
    {
        "id": "recon_utility",
        "title": "THREAT RADAR & RECON",
        "icon": "👁️",
        "accent": "#c084fc",     # Purple / Violet
        "accent_bg": "rgba(192, 132, 252, 0.12)",
        "accent_border": "rgba(192, 132, 252, 0.35)",
        "summary": [
            ("Targeting Detection", "Sensory Warning when Aimed At"),
            ("Trap Detection Radius", "800m Radius (Detect Trap)"),
            ("Trap Neutralization", "Disarm Ability Unlocked"),
            ("Hunger Proximity Radar", "2500m Radius (Smell Flesh)"),
            ("Equipment Draw Speed", "+50% Faster Swap (Quick Draw)")
        ],
        "talents": [
            {"name": "Mortal Wits", "highlight": "Sense when an Enemy is Aiming at You"},
            {"name": "Detect Trap", "highlight": "Detect Nearby Traps within 800m"},
            {"name": "Break Mechanism", "highlight": "Trap Disarming Ability Unlocked"},
            {"name": "Smell Flesh", "highlight": "Sense nearby Hunger within 2500m"},
            {"name": "Quick Draw", "highlight": "+50% Faster Item Drawing Speed"}
        ]
    }
]

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>HUNGER Companion - Level 100 Mastery Build Functional Analysis</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Inter:wght@400;500;600;700&family=Spectral:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
<style>
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}
  
  body {{
    background-color: #0b0b09;
    background-image: 
      radial-gradient(circle at 50% 0%, rgba(229, 192, 123, 0.08) 0%, transparent 60%),
      radial-gradient(circle at 10% 40%, rgba(56, 189, 248, 0.05) 0%, transparent 50%),
      radial-gradient(circle at 90% 70%, rgba(74, 222, 128, 0.05) 0%, transparent 50%),
      linear-gradient(to bottom, #070706 0%, #0e0e0b 100%);
    color: #f0ebe0;
    font-family: 'Inter', sans-serif;
    padding: 24px 30px 30px;
    width: 1820px;
    margin: 0 auto;
  }}
  
  .font-cinzel {{ font-family: 'Cinzel', serif; }}
  .font-spectral {{ font-family: 'Spectral', serif; }}

  /* TOP HEADER */
  .top-header {{
    background: #151512;
    border: 1px solid #302c24;
    border-radius: 14px;
    padding: 16px 22px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 16px 40px rgba(0,0,0,0.6);
    margin-bottom: 16px;
    position: relative;
  }}
  
  .top-header::after {{
    content: '';
    position: absolute;
    bottom: -1px;
    left: 20px;
    right: 20px;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(229, 192, 123, 0.4), transparent);
  }}
  
  .header-left {{
    display: flex;
    align-items: center;
    gap: 14px;
  }}
  
  .crest-icon {{
    width: 48px;
    height: 48px;
    border-radius: 10px;
    border: 1.5px solid rgba(229, 192, 123, 0.5);
    background: #1c1c18;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    color: #e5c07b;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
  }}
  
  .title-content {{
    display: flex;
    flex-direction: column;
    gap: 3px;
  }}
  
  .brand-tag {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  
  .tag-badge {{
    font-size: 10.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #e5c07b;
    background: rgba(229, 192, 123, 0.12);
    border: 1px solid rgba(229, 192, 123, 0.35);
    padding: 2px 8px;
    border-radius: 4px;
  }}
  
  .tag-sub {{
    font-size: 11.5px;
    color: #a8a091;
    font-family: 'Cinzel', serif;
    letter-spacing: 0.5px;
  }}
  
  .main-title {{
    font-family: 'Cinzel', serif;
    font-size: 24px;
    font-weight: 800;
    color: #e5c07b;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    line-height: 1.15;
  }}
  
  /* HEADER STAT PILLS */
  .header-stats {{
    display: flex;
    gap: 9px;
    align-items: center;
  }}
  
  .stat-pill {{
    background: #1c1c18;
    border: 1px solid #302c24;
    border-radius: 8px;
    padding: 6px 13px;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 90px;
  }}
  
  .stat-pill.highlight {{
    border-color: rgba(229, 192, 123, 0.45);
    background: rgba(229, 192, 123, 0.08);
  }}
  
  .stat-pill .num {{
    font-family: 'Cinzel', serif;
    font-size: 20px;
    font-weight: 800;
    line-height: 1;
    color: #f0ebe0;
  }}
  
  .stat-pill.highlight .num {{ color: #e5c07b; }}
  
  .stat-pill .label {{
    font-size: 9.5px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #a8a091;
    margin-top: 2px;
    font-weight: 600;
  }}

  /* HERO BENCHMARK CARDS SECTION (HUGO VS GABRIEL) */
  .hero-benchmark-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 18px;
  }}
  
  .hero-card {{
    background: #141411;
    border: 1px solid #302c24;
    border-radius: 12px;
    padding: 14px 18px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}
  
  .hero-card.hugo {{ border-top: 3.5px solid #ef4444; }}
  .hero-card.gabriel {{ border-top: 3.5px solid #38bdf8; }}
  
  .hero-top-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #28251e;
    padding-bottom: 8px;
  }}
  
  .hero-identity {{
    display: flex;
    align-items: center;
    gap: 9px;
  }}
  
  .hero-avatar-badge {{
    width: 32px;
    height: 32px;
    border-radius: 7px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    border: 1px solid rgba(255, 255, 255, 0.15);
  }}
  
  .hero-name {{
    font-family: 'Cinzel', serif;
    font-size: 17px;
    font-weight: 800;
    color: #f0ebe0;
    letter-spacing: 0.5px;
  }}
  
  .hero-role {{
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #a8a091;
  }}
  
  .hero-badge-tag {{
    font-family: 'Cinzel', serif;
    font-size: 11px;
    font-weight: 700;
    padding: 2.5px 9px;
    border-radius: 4px;
    letter-spacing: 0.5px;
  }}
  
  .hero-metrics-row {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
  }}
  
  .hero-metric-tile {{
    background: #191915;
    border: 1px solid #28251e;
    border-radius: 8px;
    padding: 8px 10px;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }}
  
  .metric-header {{
    font-size: 9.5px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #8c8373;
    font-weight: 600;
  }}
  
  .metric-value {{
    font-family: 'Cinzel', serif;
    font-size: 17px;
    font-weight: 800;
    line-height: 1.1;
  }}
  
  .metric-condition {{
    font-size: 9.5px;
    color: #a8a091;
    font-family: 'Spectral', serif;
    line-height: 1.25;
    margin-top: 1px;
  }}
  
  .hero-synergy-footer {{
    background: #0d0d0a;
    border: 1px solid #201e18;
    border-radius: 6px;
    padding: 7px 10px;
    font-size: 10.5px;
    color: #c4bcae;
    line-height: 1.35;
  }}
  
  .hero-synergy-footer strong {{ color: #e5c07b; }}

  /* FUNCTIONAL 4-COLUMN GRID */
  .functional-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    align-items: start;
  }}
  
  .cat-column {{
    background: #12120f;
    border: 1px solid #302c24;
    border-radius: 12px;
    padding: 13px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    box-shadow: 0 10px 26px rgba(0,0,0,0.5);
  }}
  
  .cat-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 8px;
    border-bottom: 1px solid #2d2921;
    margin-bottom: 2px;
  }}
  
  .cat-title-wrap {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  
  .cat-icon {{
    font-size: 15px;
  }}
  
  .cat-title {{
    font-family: 'Cinzel', serif;
    font-size: 14.5px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
  }}
  
  .cat-talent-count {{
    font-family: 'Cinzel', serif;
    font-size: 11px;
    font-weight: 700;
    padding: 1.5px 7px;
    border-radius: 12px;
  }}

  /* CATEGORY SUMMARY BOX (RIGHT AT THE TOP OF EACH CATEGORY) */
  .cat-summary-box {{
    background: #171713;
    border: 1px solid #28251e;
    border-radius: 7px;
    padding: 8px 10px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin-bottom: 4px;
  }}
  
  .cat-summary-row {{
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    border-bottom: 1px dashed #22201a;
    padding-bottom: 2.5px;
  }}
  
  .cat-summary-lbl {{
    color: #8c8373;
    font-weight: 500;
  }}
  
  .cat-summary-val {{
    font-weight: 700;
    font-family: 'Cinzel', serif;
    font-size: 10.5px;
  }}

  /* TALENT CARDS INSIDE CATEGORIES */
  .talent-card {{
    background: #161612;
    border: 1px solid #26231c;
    border-radius: 7px;
    padding: 7px 9px;
    display: flex;
    gap: 9px;
    align-items: flex-start;
    position: relative;
  }}
  
  .talent-card.keystone {{
    background: linear-gradient(135deg, rgba(229, 192, 123, 0.14), #161612 70%);
    border: 1px solid rgba(229, 192, 123, 0.55);
    box-shadow: 0 0 12px rgba(229, 192, 123, 0.1);
  }}
  
  .talent-icon-box {{
    position: relative;
    flex-shrink: 0;
    width: 40px;
    height: 40px;
    background: #090907;
    border-radius: 5px;
    border: 1px solid #332f27;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.5);
  }}
  
  .talent-icon-box img {{
    width: 32px;
    height: 32px;
    object-fit: contain;
  }}
  
  .tree-pill {{
    position: absolute;
    bottom: -3px;
    right: -3px;
    background: #090907;
    border: 1px solid #453f32;
    color: #8c8373;
    font-family: 'Cinzel', serif;
    font-size: 8px;
    font-weight: 700;
    padding: 0px 3px;
    border-radius: 2px;
    line-height: 1.1;
  }}
  
  .talent-content {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 1.5px;
  }}
  
  .talent-top {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
  }}
  
  .talent-name {{
    font-family: 'Cinzel', serif;
    font-size: 13px;
    font-weight: 700;
    color: #f0ebe0;
    letter-spacing: 0.3px;
  }}
  
  .rank-badge {{
    font-family: 'Cinzel', serif;
    font-size: 9.5px;
    font-weight: 700;
    padding: 1px 5px;
    border-radius: 3px;
    letter-spacing: 0.5px;
  }}
  
  .rank-max {{
    background: rgba(229, 192, 123, 0.15);
    color: #e5c07b;
    border: 1px solid rgba(229, 192, 123, 0.4);
  }}
  
  .rank-single {{
    background: rgba(168, 85, 247, 0.15);
    color: #c084fc;
    border: 1px solid rgba(168, 85, 247, 0.4);
  }}
  
  .rank-partial {{
    background: rgba(56, 189, 248, 0.12);
    color: #38bdf8;
    border: 1px solid rgba(56, 189, 248, 0.35);
  }}
  
  .talent-benefit {{
    font-size: 10.5px;
    font-weight: 600;
    line-height: 1.2;
  }}
  
  .talent-card.keystone .talent-benefit {{
    color: #e5c07b;
    font-weight: 700;
  }}
  
  .talent-game-desc {{
    font-size: 9.5px;
    color: #8c8373;
    line-height: 1.25;
    font-family: 'Spectral', serif;
  }}
</style>
</head>
<body>

  <!-- TOP HEADER -->
  <header class="top-header">
    <div class="header-left">
      <div class="crest-icon font-cinzel">⚔</div>
      <div class="title-content">
        <div class="brand-tag">
          <span class="tag-badge font-cinzel">HUNGER COMPANION</span>
          <span class="tag-sub">Mastery Progression // Grouped by Combat Function</span>
        </div>
        <h1 class="main-title">LEVEL 100 MASTERY BUILD // TWO-HANDED BRAWLER &amp; SURVIVOR</h1>
      </div>
    </div>
    
    <!-- Badges / Points -->
    <div class="header-stats">
      <div class="stat-pill highlight">
        <span class="num">91 / 91</span>
        <span class="label">Points (100%)</span>
      </div>
      <div class="stat-pill">
        <span class="num" style="color: #38bdf8;">18</span>
        <span class="label">Physiology</span>
      </div>
      <div class="stat-pill">
        <span class="num" style="color: #4ade80;">36</span>
        <span class="label">Survival</span>
      </div>
      <div class="stat-pill">
        <span class="num" style="color: #e5c07b;">37</span>
        <span class="label">Arms</span>
      </div>
      <div class="stat-pill">
        <span class="num" style="color: #645e52;">0</span>
        <span class="label">Cunning</span>
      </div>
      <div class="stat-pill">
        <span class="num" style="color: #645e52;">0</span>
        <span class="label">Martial</span>
      </div>
    </div>
  </header>

  <!-- HERO BENCHMARK COMPARISON: HUGO VS GABRIEL -->
  <div class="hero-benchmark-grid">
  
    <!-- HUGO CARD -->
    <div class="hero-card hugo">
      <div class="hero-top-bar">
        <div class="hero-identity">
          <div class="hero-avatar-badge" style="background: rgba(239, 68, 68, 0.15); color: #f87171; border-color: rgba(239, 68, 68, 0.4);">
            🩸
          </div>
          <div>
            <div class="hero-name">HUGO <span style="font-size:12px; color:#ef4444; font-weight:600;">(THE MANIAC)</span></div>
            <div class="hero-role">Burst Projectile Negator &amp; Peak Movespeed Striker</div>
          </div>
        </div>
        <div class="hero-badge-tag" style="background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4);">
          MAX MOVESPEED: +31%
        </div>
      </div>
      
      <div class="hero-metrics-row">
        <div class="hero-metric-tile">
          <span class="metric-header">Max Movement Speed</span>
          <span class="metric-value" style="color: #f87171;">+31% FLAT</span>
          <span class="metric-condition">Taste of Blood (+8%) + Overlander (+8% 2H drawn) + Shock (+15% on hit)</span>
        </div>
        <div class="hero-metric-tile">
          <span class="metric-header">Max Tanking / Ranged EHP</span>
          <span class="metric-value" style="color: #fbbf24;">416.7 EHP + ZEALOT</span>
          <span class="metric-condition">40% Projectile DR (Maniac 25% + Berzerker 20%) &amp; 100% 1-Shot Absorb (Zealot)</span>
        </div>
        <div class="hero-metric-tile">
          <span class="metric-header">Sustain &amp; Self-Repair</span>
          <span class="metric-value" style="color: #4ade80;">50% REPAIR HEAL</span>
          <span class="metric-condition">Toughen Up heals 50% of armour repaired (+50% repair tool speed via Fastening)</span>
        </div>
      </div>
      
      <div class="hero-synergy-footer">
        <strong>Hugo Synergy:</strong> Absorbs 100% of the deadliest sniper shot via <em>Zealot</em> (0 dmg taken), gains universal <strong>25% All-Damage DR</strong> via <em>Maniac</em> (stacking to <strong>40% DR vs projectiles</strong> with <em>Berzerker</em>), and moves at a continuous <strong>+31% movespeed</strong> with <strong>+25% 2H lunge velocity</strong>.
      </div>
    </div>

    <!-- GABRIEL CARD -->
    <div class="hero-card gabriel">
      <div class="hero-top-bar">
        <div class="hero-identity">
          <div class="hero-avatar-badge" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; border-color: rgba(56, 189, 248, 0.4);">
            🛡
          </div>
          <div>
            <div class="hero-name">GABRIEL <span style="font-size:12px; color:#38bdf8; font-weight:600;">(SOLDIER OF FORTUNE)</span></div>
            <div class="hero-role">Sustained 15s Brawler &amp; 30% Life-Leech Tank</div>
          </div>
        </div>
        <div class="hero-badge-tag" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.4);">
          MAX SPRINT: +29%
        </div>
      </div>
      
      <div class="hero-metrics-row">
        <div class="hero-metric-tile">
          <span class="metric-header">Max Sprint Speed</span>
          <span class="metric-value" style="color: #38bdf8;">+29% SPRINT</span>
          <span class="metric-condition">Charge (+6% sprint) + Overlander (+8% 2H drawn) + Shock (+15% on hit)</span>
        </div>
        <div class="hero-metric-tile">
          <span class="metric-header">Max Tanking / Ranged EHP</span>
          <span class="metric-value" style="color: #fbbf24;">416.7 EHP (15 SEC)</span>
          <span class="metric-condition">40% Projectile DR (Line Infantry 25% + Berzerker 20%) sustained for 15 full seconds</span>
        </div>
        <div class="hero-metric-tile">
          <span class="metric-header">Sustain &amp; Life-Leech</span>
          <span class="metric-value" style="color: #4ade80;">+30% LIFE-LEECH</span>
          <span class="metric-condition">Sadist returns 30% of all damage dealt as HP for 15s + 50% armour repair heal</span>
        </div>
      </div>
      
      <div class="hero-synergy-footer">
        <strong>Gabriel Synergy:</strong> Combines <strong>15 seconds of 40% Ranged DR</strong> (*Line Infantry* + *Berzerker*) with <strong>Sadist 30% Life-Leech</strong>. Because 2H attacks consume -25% Light/Heavy/Sprint energy and regen starts 50% faster, Gabriel relentlessly cleaves targets to regenerate 150+ HP mid-fight.
      </div>
    </div>
    
  </div>

  <!-- FUNCTIONAL 4-COLUMN TALENTS GRID -->
  <div class="functional-grid">
"""

tree_letters = {
    "physiology": "P",
    "survival": "S",
    "arms": "A"
}

for cat in categories:
    cat_id = cat["id"]
    cat_title = cat["title"]
    cat_icon = cat["icon"]
    accent = cat["accent"]
    accent_bg = cat["accent_bg"]
    accent_border = cat["accent_border"]
    talent_list = cat["talents"]
    
    html += f"""
    <!-- CATEGORY: {cat_title} -->
    <div class="cat-column">
      <div class="cat-header">
        <div class="cat-title-wrap">
          <span class="cat-icon">{cat_icon}</span>
          <span class="cat-title" style="color: {accent};">{cat_title}</span>
        </div>
        <span class="cat-talent-count" style="background: {accent_bg}; color: {accent}; border: 1px solid {accent_border};">
          {len(talent_list)} TALENTS
        </span>
      </div>
      
      <!-- Dedicated Category Summary -->
      <div class="cat-summary-box">
    """
    
    for lbl, val in cat["summary"]:
        html += f"""
        <div class="cat-summary-row">
          <span class="cat-summary-lbl">{lbl}</span>
          <span class="cat-summary-val" style="color: {accent};">{val}</span>
        </div>
        """
        
    html += """
      </div>
    """
    
    # Render talent cards
    for item in talent_list:
        t_name = item["name"]
        t = all_talents.get(t_name)
        if not t:
            continue
            
        rank = t['rank']
        max_r = t['max']
        tier = t['tier']
        icon_file = t['icon']
        b64_src = icons_b64.get(icon_file, "")
        tree_slug = t['tree_slug']
        t_let = tree_letters.get(tree_slug, "T")
        
        is_keystone = (tier == 8)
        keystone_class = " keystone" if is_keystone else ""
        
        if rank == max_r and max_r > 1:
            rank_class = "rank-max"
            rank_text = f"{rank}/{max_r} MAX"
        elif max_r == 1:
            rank_class = "rank-single"
            rank_text = "UNLOCKED"
        else:
            rank_class = "rank-partial"
            rank_text = f"{rank}/{max_r}"
            
        highlight = item["highlight"]
        highlight_color = accent if not is_keystone else "#e5c07b"
        
        html += f"""
      <div class="talent-card{keystone_class}">
        <div class="talent-icon-box" style="border-color: {accent_border};">
          <img src="{b64_src}" alt="{t_name}">
          <div class="tree-pill">{t_let}-T{ROMAN[tier]}</div>
        </div>
        <div class="talent-content">
          <div class="talent-top">
            <span class="talent-name">{t_name}</span>
            <span class="rank-badge {rank_class}">{rank_text}</span>
          </div>
          <div class="talent-benefit" style="color: {highlight_color};">{highlight}</div>
          <div class="talent-game-desc">{t['desc']}</div>
        </div>
      </div>
        """
        
    html += """
    </div>
    """

html += """
  </div>

</body>
</html>
"""

with open('mastery_build_card.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Generated functionally-grouped HTML successfully!")
