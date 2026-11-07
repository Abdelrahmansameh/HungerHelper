from bs4 import BeautifulSoup
import sys
sys.stdout.reconfigure(encoding='utf-8')

for hero in ['gabriel', 'hugo']:
    print(f"\n==================== {hero.upper()} ====================")
    with open(f'{hero}_page.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Print headings, ability descriptions, stats
    main = soup.find('main') or soup.find('body')
    if main:
        for section in main.find_all(['section', 'article', 'div'], recursive=True):
            cls = section.get('class', [])
            txt = section.get_text(separator=' | ', strip=True)
            if any(k in txt.lower() for k in ['passive', 'tactical', 'ultimate', 'health', 'speed', 'charge', 'maniac', 'taste of blood']):
                if len(txt) < 800 and len(txt) > 50:
                    print(txt)
                    print('-'*30)
