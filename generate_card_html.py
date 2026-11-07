import json
import base64
import os
import subprocess
from PIL import Image

with open('user_talents_summary.json', 'r', encoding='utf-8') as f:
    trees = json.load(f)

# Convert each icon to base64
icons_b64 = {}
for root, dirs, files in os.walk('talent_icons'):
    for file in files:
        if file.endswith('.png'):
            with open(os.path.join(root, file), 'rb') as img_f:
                icons_b64[file] = "data:image/png;base64," + base64.b64encode(img_f.read()).decode('ascii')

ACTIVE_HIGHLIGHTS = {
    "Endurance": "-30% Sprint Stamina Drain",
    "Catching Breath": "Stamina Recovery begins 100% Sooner (Instant)",
    "Leap": "-40% Jump & Vault Stamina Cost",
    "Oxygenation": "+30% Faster Stamina Recovery Rate",
    
    "Surgeon": "+30% Faster Downed Player Revive",
    "Detect Trap": "Detect Traps within 800m Radius",
    "Leg Armour": "Equip Leg Armour Unlocked (Full 3-Pc)",
    "Quick Draw": "+50% Faster Item Drawing Speed",
    "Fastening": "+50% Faster Armour Repair Tool Speed",
    "Relentless": "Restore 20 Energy on Down/Kill",
    "Smell Flesh": "Sense nearby Hunger within 2500m Radius",
    "Operation": "+18% Extra Healing from Medicines",
    "Break Mechanism": "Trap Disarming Ability Unlocked",
    "Mortal Wits": "Sense when an Enemy is Aiming at You",
    "Shock": "+15% Move Speed for 20s when Damaged",
    "Toughen Up": "★ KEYSTONE: Heal for 50% of Armour Repaired",
    
    "Fencing": "Melee Attacks Gain Forward Lunge",
    "Overlander": "+8% Move Speed with 2H Melee Drawn",
    "Deft Strikes": "-25% Light Attack Energy Cost (2H Melee)",
    "Blitz": "-25% Sprint Attack Energy Cost (Melee)",
    "Phalanx": "Energy Regen Starts 50% Faster",
    "Expert Strikes": "-25% Heavy Attack Energy Cost (2H Melee)",
    "Guard Recovery": "+25% Faster Energy Regen Rate",
    "Limber": "+16% 1H Melee Lunge Speed",
    "Advanced Footwork": "+25% 2H Melee Lunge Speed",
    "Berzerker": "★ KEYSTONE: -20% Projectile Dmg Taken (Dual Melee)"
}

ROMAN = ["0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]

tree_themes = {
    "Physiology": {
        "accent": "#4ade80",      # Emerald / Mint
        "accent_bg": "rgba(74, 222, 128, 0.12)",
        "accent_border": "rgba(74, 222, 128, 0.35)",
        "badge_border": "#4ade80"
    },
    "Survival": {
        "accent": "#a3e635",      # Lime / Forest Survival
        "accent_bg": "rgba(163, 230, 53, 0.12)",
        "accent_border": "rgba(163, 230, 53, 0.35)",
        "badge_border": "#a3e635"
    },
    "Arms": {
        "accent": "#e5c07b",      # Hunger Companion Signature Gold
        "accent_bg": "rgba(229, 192, 123, 0.14)",
        "accent_border": "rgba(229, 192, 123, 0.45)",
        "badge_border": "#e5c07b"
    }
}

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>HUNGER Companion - Level 100 Mastery Progression & Combat Benchmarks</title>
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
      radial-gradient(circle at 10% 30%, rgba(74, 222, 128, 0.04) 0%, transparent 50%),
      radial-gradient(circle at 90% 60%, rgba(229, 192, 123, 0.05) 0%, transparent 50%),
      linear-gradient(to bottom, #070706 0%, #0e0e0b 100%);
    color: #f0ebe0;
    font-family: 'Inter', sans-serif;
    padding: 28px 34px 34px;
    width: 1780px;
    margin: 0 auto;
  }}
  
  .font-cinzel {{ font-family: 'Cinzel', serif; }}
  .font-spectral {{ font-family: 'Spectral', serif; }}

  /* TOP HEADER */
  .top-header {{
    background: #151512;
    border: 1px solid #302c24;
    border-radius: 16px;
    padding: 18px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 16px 40px rgba(0,0,0,0.6);
    margin-bottom: 20px;
    position: relative;
  }}
  
  .top-header::after {{
    content: '';
    position: absolute;
    bottom: -1px;
    left: 24px;
    right: 24px;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(229, 192, 123, 0.4), transparent);
  }}
  
  .header-left {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}
  
  .crest-icon {{
    width: 52px;
    height: 52px;
    border-radius: 12px;
    border: 1.5px solid rgba(229, 192, 123, 0.5);
    background: #1c1c18;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    color: #e5c07b;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
  }}
  
  .title-content {{
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}
  
  .brand-tag {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  
  .tag-badge {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #e5c07b;
    background: rgba(229, 192, 123, 0.12);
    border: 1px solid rgba(229, 192, 123, 0.35);
    padding: 2px 10px;
    border-radius: 4px;
  }}
  
  .tag-sub {{
    font-size: 12px;
    color: #a8a091;
    font-family: 'Cinzel', serif;
    letter-spacing: 0.5px;
  }}
  
  .main-title {{
    font-family: 'Cinzel', serif;
    font-size: 26px;
    font-weight: 800;
    color: #e5c07b;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    line-height: 1.15;
  }}
  
  /* HEADER STAT PILLS */
  .header-stats {{
    display: flex;
    gap: 10px;
    align-items: center;
  }}
  
  .stat-pill {{
    background: #1c1c18;
    border: 1px solid #302c24;
    border-radius: 10px;
    padding: 7px 14px;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 95px;
  }}
  
  .stat-pill.highlight {{
    border-color: rgba(229, 192, 123, 0.45);
    background: rgba(229, 192, 123, 0.08);
  }}
  
  .stat-pill .num {{
    font-family: 'Cinzel', serif;
    font-size: 22px;
    font-weight: 800;
    line-height: 1;
    color: #f0ebe0;
  }}
  
  .stat-pill.highlight .num {{ color: #e5c07b; }}
  
  .stat-pill .label {{
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #a8a091;
    margin-top: 3px;
    font-weight: 600;
  }}

  /* HERO BENCHMARK CARDS SECTION (HUGO VS GABRIEL) */
  .hero-benchmark-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
    margin-bottom: 20px;
  }}
  
  .hero-card {{
    background: #141411;
    border: 1px solid #302c24;
    border-radius: 12px;
    padding: 16px 20px;
    position: relative;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
    display: flex;
    flex-direction: column;
    gap: 12px;
  }}
  
  .hero-card.hugo {{
    border-top: 3.5px solid #ef4444;
  }}
  
  .hero-card.gabriel {{
    border-top: 3.5px solid #38bdf8;
  }}
  
  .hero-top-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #28251e;
    padding-bottom: 10px;
  }}
  
  .hero-identity {{
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  
  .hero-avatar-badge {{
    width: 34px;
    height: 34px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    border: 1px solid rgba(255, 255, 255, 0.15);
  }}
  
  .hero-name {{
    font-family: 'Cinzel', serif;
    font-size: 19px;
    font-weight: 800;
    color: #f0ebe0;
    letter-spacing: 0.5px;
  }}
  
  .hero-role {{
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #a8a091;
  }}
  
  .hero-badge-tag {{
    font-family: 'Cinzel', serif;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 4px;
    letter-spacing: 0.5px;
  }}
  
  .hero-metrics-row {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
  }}
  
  .hero-metric-tile {{
    background: #191915;
    border: 1px solid #28251e;
    border-radius: 8px;
    padding: 10px 12px;
    display: flex;
    flex-direction: column;
    gap: 3px;
  }}
  
  .metric-header {{
    font-size: 10.5px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #8c8373;
    font-weight: 600;
  }}
  
  .metric-value {{
    font-family: 'Cinzel', serif;
    font-size: 19px;
    font-weight: 800;
    line-height: 1.1;
  }}
  
  .metric-condition {{
    font-size: 10px;
    color: #a8a091;
    font-family: 'Spectral', serif;
    line-height: 1.3;
    margin-top: 2px;
  }}
  
  .hero-synergy-footer {{
    background: #0d0d0a;
    border: 1px solid #201e18;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 11px;
    color: #c4bcae;
    line-height: 1.4;
  }}
  
  .hero-synergy-footer strong {{
    color: #e5c07b;
  }}

  /* THREE COLUMN TREE LAYOUT */
  .trees-grid {{
    display: grid;
    grid-template-columns: 1.05fr 1.32fr 1.32fr;
    gap: 18px;
    margin-bottom: 20px;
    align-items: start;
  }}
  
  .tree-panel {{
    background: #12120f;
    border: 1px solid #302c24;
    border-radius: 14px;
    padding: 15px;
    display: flex;
    flex-direction: column;
    gap: 9px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.5);
  }}
  
  .tree-panel-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 10px;
    border-bottom: 1px solid #2d2921;
    margin-bottom: 2px;
  }}
  
  .tree-label {{
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  
  .tree-icon-box {{
    width: 26px;
    height: 26px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
  }}
  
  .tree-name {{
    font-family: 'Cinzel', serif;
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
  }}
  
  .tree-pts-tag {{
    font-family: 'Cinzel', serif;
    font-size: 12.5px;
    font-weight: 700;
    padding: 2.5px 10px;
    border-radius: 20px;
    letter-spacing: 0.5px;
  }}

  /* TALENT ITEM CARDS */
  .talent-item {{
    background: #171713;
    border: 1px solid #28251e;
    border-radius: 8px;
    padding: 8px 11px;
    display: flex;
    gap: 11px;
    align-items: flex-start;
    position: relative;
  }}
  
  .talent-item.keystone {{
    background: linear-gradient(135deg, rgba(229, 192, 123, 0.15), #171713 70%);
    border: 1.5px solid rgba(229, 192, 123, 0.6);
    box-shadow: 0 0 16px rgba(229, 192, 123, 0.14);
  }}
  
  .talent-img-box {{
    position: relative;
    flex-shrink: 0;
    width: 46px;
    height: 46px;
    background: #0b0b09;
    border-radius: 6px;
    border: 1px solid #3d372c;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 3px 8px rgba(0,0,0,0.6);
  }}
  
  .talent-img-box img {{
    width: 38px;
    height: 38px;
    object-fit: contain;
  }}
  
  .tier-chip {{
    position: absolute;
    bottom: -4px;
    right: -4px;
    background: #0b0b09;
    border: 1px solid #504837;
    color: #a8a091;
    font-family: 'Cinzel', serif;
    font-size: 9px;
    font-weight: 700;
    padding: 0px 4px;
    border-radius: 3px;
    line-height: 1.2;
  }}
  
  .talent-body {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }}
  
  .talent-heading {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
  }}
  
  .talent-title {{
    font-family: 'Cinzel', serif;
    font-size: 14.5px;
    font-weight: 700;
    color: #f0ebe0;
    letter-spacing: 0.5px;
  }}
  
  .rank-pill {{
    font-family: 'Cinzel', serif;
    font-size: 10.5px;
    font-weight: 700;
    padding: 1px 6px;
    border-radius: 4px;
    letter-spacing: 0.5px;
  }}
  
  .rank-pill.max {{
    background: rgba(229, 192, 123, 0.15);
    color: #e5c07b;
    border: 1px solid rgba(229, 192, 123, 0.4);
  }}
  
  .rank-pill.single {{
    background: rgba(168, 85, 247, 0.15);
    color: #c084fc;
    border: 1px solid rgba(168, 85, 247, 0.4);
  }}
  
  .rank-pill.partial {{
    background: rgba(74, 222, 128, 0.12);
    color: #4ade80;
    border: 1px solid rgba(74, 222, 128, 0.35);
  }}
  
  .talent-highlight {{
    font-size: 11.5px;
    font-weight: 600;
    line-height: 1.25;
  }}
  
  .talent-item.keystone .talent-highlight {{
    color: #e5c07b;
    font-weight: 700;
  }}
  
  .talent-raw-desc {{
    font-size: 10px;
    color: #9c9484;
    line-height: 1.35;
    margin-top: 1px;
    font-family: 'Spectral', serif;
  }}

  /* STAT MULTIPLIERS CARD IN LEFT COLUMN */
  .multipliers-card {{
    background: #171713;
    border: 1px solid #302c24;
    border-radius: 8px;
    padding: 12px 14px;
    margin-top: 4px;
    display: flex;
    flex-direction: column;
    gap: 7px;
  }}
  
  .multipliers-header {{
    font-family: 'Cinzel', serif;
    font-size: 13.5px;
    font-weight: 700;
    color: #e5c07b;
    letter-spacing: 1px;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 6px;
    border-bottom: 1px solid #28251e;
    padding-bottom: 5px;
  }}
  
  .stat-entry {{
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    border-bottom: 1px dashed #24221b;
    padding-bottom: 3px;
  }}
  
  .stat-entry-lbl {{ color: #a8a091; }}
  
  .stat-entry-val {{
    font-weight: 700;
    font-family: 'Cinzel', serif;
    font-size: 11.5px;
    letter-spacing: 0.5px;
  }}
  
  .val-gold {{ color: #e5c07b; }}
  .val-mint {{ color: #4ade80; }}
  .val-lime {{ color: #a3e635; }}

  .tree-zero-card {{
    background: #0f0f0c;
    border: 1px dashed #28251e;
    border-radius: 6px;
    padding: 7px 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 11px;
    color: #7a7265;
  }}

  /* CUMULATIVE COMBAT BENCHMARKS DASHBOARD */
  .combat-benchmarks-footer {{
    background: #12120f;
    border: 1px solid #302c24;
    border-radius: 14px;
    padding: 16px 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
  }}
  
  .benchmark-panel {{
    background: #171713;
    border: 1px solid #28251e;
    border-top: 3px solid #e5c07b;
    border-radius: 8px;
    padding: 12px 14px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}
  
  .benchmark-title {{
    font-family: 'Cinzel', serif;
    font-size: 13.5px;
    font-weight: 700;
    color: #e5c07b;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }}
  
  .benchmark-list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 11px;
    color: #b8b0a0;
    font-family: 'Spectral', serif;
  }}
  
  .benchmark-list li {{
    display: flex;
    align-items: baseline;
    gap: 6px;
  }}
  
  .benchmark-list li::before {{
    content: '▪';
    color: #e5c07b;
    font-size: 10px;
  }}
  
  .benchmark-list strong {{
    color: #f0ebe0;
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
          <span class="tag-sub">Mastery Progression &amp; Full Combat Recon</span>
        </div>
        <h1 class="main-title">LEVEL 100 MASTERY BUILD // TWO-HANDED BRAWLER &amp; SURVIVOR</h1>
      </div>
    </div>
    
    <!-- Badges / Stats -->
    <div class="header-stats">
      <div class="stat-pill highlight">
        <span class="num">91 / 91</span>
        <span class="label">Points (100%)</span>
      </div>
      <div class="stat-pill">
        <span class="num" style="color: #4ade80;">18</span>
        <span class="label">Physiology</span>
      </div>
      <div class="stat-pill">
        <span class="num" style="color: #a3e635;">36</span>
        <span class="label">Survival</span>
      </div>
      <div class="stat-pill">
        <span class="num" style="color: #e5c07b;">37</span>
        <span class="label">Arms</span>
      </div>
      <div class="stat-pill">
        <span class="num" style="color: #7a7265;">0</span>
        <span class="label">Cunning</span>
      </div>
      <div class="stat-pill">
        <span class="num" style="color: #7a7265;">0</span>
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
            <div class="hero-name">HUGO <span style="font-size:13px; color:#ef4444; font-weight:600;">(THE MANIAC)</span></div>
            <div class="hero-role">Burst Projectile Negator &amp; Maximum Speed Striker</div>
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
        <strong>Hugo Combat Synergy:</strong> Absorbs 100% of the deadliest sniper shot via <em>Zealot</em> (0 damage taken), gains universal <strong>25% All-Damage DR</strong> via <em>Maniac</em> (stacking to <strong>40% DR vs projectiles</strong> with <em>Berzerker</em>), and closes distance at a blisteringly fast <strong>+31% continuous movespeed</strong> with <strong>+25% 2H lunge velocity</strong>.
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
            <div class="hero-name">GABRIEL <span style="font-size:13px; color:#38bdf8; font-weight:600;">(SOLDIER OF FORTUNE)</span></div>
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
        <strong>Gabriel Combat Synergy:</strong> Combines <strong>15 seconds of 40% Ranged DR</strong> (*Line Infantry* + *Berzerker*) with <strong>Sadist 30% Life-Leech</strong>. Because 2H attacks consume -25% Light/Heavy/Sprint energy and regen starts 50% faster, Gabriel relentlessly cleaves targets to regenerate 150+ HP mid-fight while healing 50% of repaired armour.
      </div>
    </div>
    
  </div>

  <!-- MAIN TREES CONTAINER -->
  <div class="trees-grid">
"""

tree_icons_map = {
    "Physiology": "⚡",
    "Survival": "🛡",
    "Arms": "⚔"
}

for tree in trees:
    slug = tree['slug']
    name = tree['name']
    points = tree['points']
    theme = tree_themes.get(name, {
        "accent": "#e5c07b",
        "accent_bg": "rgba(229, 192, 123, 0.12)",
        "accent_border": "rgba(229, 192, 123, 0.35)",
        "badge_border": "#e5c07b"
    })
    tree_icon = tree_icons_map.get(name, "✦")
    
    html += f"""
    <!-- {name} TREE -->
    <div class="tree-panel">
      <div class="tree-panel-header">
        <div class="tree-label">
          <div class="tree-icon-box" style="background: {theme['accent_bg']}; border: 1px solid {theme['accent_border']}; color: {theme['accent']};">
            {tree_icon}
          </div>
          <div class="tree-name" style="color: {theme['accent']};">{name}</div>
        </div>
        <div class="tree-pts-tag" style="background: {theme['accent_bg']}; color: {theme['accent']}; border: 1px solid {theme['accent_border']};">
          {points} POINTS
        </div>
      </div>
    """
    
    for t in tree['talents']:
        t_name = t['name']
        rank = t['rank']
        max_r = t['max']
        tier = t['tier']
        icon_file = t['icon']
        b64_src = icons_b64.get(icon_file, "")
        
        is_keystone = (tier == 8)
        keystone_class = " keystone" if is_keystone else ""
        
        if rank == max_r and max_r > 1:
            rank_class = "max"
            rank_text = f"{rank}/{max_r} MAX"
        elif max_r == 1:
            rank_class = "single"
            rank_text = "UNLOCKED"
        else:
            rank_class = "partial"
            rank_text = f"{rank}/{max_r}"
            
        highlight = ACTIVE_HIGHLIGHTS.get(t_name, t['desc'])
        highlight_color = theme['accent'] if not is_keystone else "#e5c07b"
        
        html += f"""
      <div class="talent-item{keystone_class}">
        <div class="talent-img-box" style="border-color: {theme['accent_border']};">
          <img src="{b64_src}" alt="{t_name}">
          <div class="tier-chip">T-{ROMAN[tier]}</div>
        </div>
        <div class="talent-body">
          <div class="talent-heading">
            <span class="talent-title">{t_name}</span>
            <span class="rank-pill {rank_class}">{rank_text}</span>
          </div>
          <div class="talent-highlight" style="color: {highlight_color};">{highlight}</div>
          <div class="talent-raw-desc">{t['desc']}</div>
        </div>
      </div>
        """
        
    if slug == "physiology":
        html += """
      <!-- Cumulative Multipliers Box -->
      <div class="multipliers-card">
        <div class="multipliers-header font-cinzel">✦ Cumulative Build Totals</div>
        <div class="stat-entry">
          <span class="stat-entry-lbl">2H Melee Lunge Velocity</span>
          <span class="stat-entry-val val-gold">+25% Velocity</span>
        </div>
        <div class="stat-entry">
          <span class="stat-entry-lbl">2H Movespeed (Weapon Drawn)</span>
          <span class="stat-entry-val val-gold">+8% Move Speed</span>
        </div>
        <div class="stat-entry">
          <span class="stat-entry-lbl">2H Light &amp; Heavy Energy Cost</span>
          <span class="stat-entry-val val-gold">-25% Stamina Drain</span>
        </div>
        <div class="stat-entry">
          <span class="stat-entry-lbl">Sprint Attack Energy Cost</span>
          <span class="stat-entry-val val-gold">-25% Stamina Drain</span>
        </div>
        <div class="stat-entry">
          <span class="stat-entry-lbl">Energy Regen Start Delay</span>
          <span class="stat-entry-val val-mint">50% Faster Start</span>
        </div>
        <div class="stat-entry">
          <span class="stat-entry-lbl">Energy Regeneration Rate</span>
          <span class="stat-entry-val val-mint">+25% Regen Rate</span>
        </div>
        <div class="stat-entry">
          <span class="stat-entry-lbl">Sprinting Stamina Drain</span>
          <span class="stat-entry-val val-mint">-30% Drain</span>
        </div>
        <div class="stat-entry">
          <span class="stat-entry-lbl">Jump &amp; Vault Stamina Cost</span>
          <span class="stat-entry-val val-mint">-40% Cost</span>
        </div>
        <div class="stat-entry">
          <span class="stat-entry-lbl">Stamina Recovery Delay</span>
          <span class="stat-entry-val val-mint">100% Sooner (Instant)</span>
        </div>
        <div class="stat-entry">
          <span class="stat-entry-lbl">Armour Repair In-Combat</span>
          <span class="stat-entry-val val-lime">+50% Speed &amp; 50% Heal</span>
        </div>
        <div class="stat-entry">
          <span class="stat-entry-lbl">Incoming Projectile DR</span>
          <span class="stat-entry-val val-lime">-20% (Dual Melee)</span>
        </div>
        <div class="stat-entry">
          <span class="stat-entry-lbl">Downed Teammate Revive</span>
          <span class="stat-entry-val val-lime">+30% Faster</span>
        </div>
      </div>
      
      <div class="tree-zero-card">
        <span>Cunning Tree: <strong style="color:#a8a091;">0 pts</strong></span>
        <span>•</span>
        <span>Martial Tree: <strong style="color:#a8a091;">0 pts</strong></span>
      </div>
        """
        
    html += """
    </div>
    """

html += """
  </div>

  <!-- FOOTER COMBAT BENCHMARKS DASHBOARD -->
  <div class="combat-benchmarks-footer">
    <div class="benchmark-panel" style="border-top-color: #ef4444;">
      <div class="benchmark-title">Hugo Peak Mobility (+31%)</div>
      <ul class="benchmark-list">
        <li><strong>+8%</strong> Taste of Blood (Melee drawn)</li>
        <li><strong>+8%</strong> Overlander (2H melee drawn)</li>
        <li><strong>+15%</strong> Shock (20s on taking hit)</li>
        <li><strong>+25%</strong> Lunge velocity on attacks</li>
        <li><strong>Condition:</strong> 2H drawn + hit taken</li>
      </ul>
    </div>
    
    <div class="benchmark-panel" style="border-top-color: #38bdf8;">
      <div class="benchmark-title">Gabriel Peak Sprint (+29%)</div>
      <ul class="benchmark-list">
        <li><strong>+6%</strong> Charge passive (Sprinting)</li>
        <li><strong>+8%</strong> Overlander (2H melee drawn)</li>
        <li><strong>+15%</strong> Shock (20s on taking hit)</li>
        <li><strong>+25%</strong> Lunge velocity on attacks</li>
        <li><strong>Condition:</strong> 2H drawn + sprinting + hit</li>
      </ul>
    </div>
    
    <div class="benchmark-panel" style="border-top-color: #a3e635;">
      <div class="benchmark-title">Max EHP &amp; Tanking</div>
      <ul class="benchmark-list">
        <li><strong>40% Ranged DR:</strong> Berzerker (20%) + Hero</li>
        <li><strong>Base Pool:</strong> 250 (100 HP + 150 3-Pc Armor)</li>
        <li><strong>Max Ranged EHP:</strong> <strong>416.7 EHP</strong></li>
        <li><strong>Hugo Burst:</strong> 100% 1-Shot Absorb (Zealot)</li>
        <li><strong>Gabriel Sustain:</strong> 15s 40% DR + 30% Leech</li>
      </ul>
    </div>
    
    <div class="benchmark-panel" style="border-top-color: #e5c07b;">
      <div class="benchmark-title">Self-Sustain &amp; Radar</div>
      <ul class="benchmark-list">
        <li><strong>Toughen Up:</strong> Heal 50% of armour repaired</li>
        <li><strong>Fastening:</strong> +50% faster repair tool speed</li>
        <li><strong>Operation:</strong> +18% bonus medical healing</li>
        <li><strong>Mortal Wits:</strong> Warns when aimed at</li>
        <li><strong>Recon Radar:</strong> 800m traps, 2500m Hunger</li>
      </ul>
    </div>
  </div>

</body>
</html>
"""

with open('mastery_build_card.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Generated full combat benchmarks & hero comparison HTML successfully!")
