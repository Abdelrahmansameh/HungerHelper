from bs4 import BeautifulSoup
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('characters_page.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

for card in soup.find_all(class_=lambda c: c and 'character' in c.lower()):
    print("Found character card:", card.get('id', card.get('class')))
    print(card.get_text(separator=' | ', strip=True)[:300])
    print('='*40)

# If no class='character', let's search for text Hugo and Gabriel
for tag in soup.find_all(['div', 'article', 'section']):
    txt = tag.get_text()
    if 'Hugo' in txt and 'Gabriel' in txt and len(txt) < 3000:
        print("Found container with both:")
        print(tag.get_text(separator='\n', strip=True)[:1000])
        break
