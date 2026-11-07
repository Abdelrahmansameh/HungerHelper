from bs4 import BeautifulSoup
import json

with open("bestiary_page.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

print("Title:", soup.title.string if soup.title else "No title")

# Find images
imgs = [img.get("src") for img in soup.find_all("img") if img.get("src")]
print(f"Found {len(imgs)} images:")
for img in imgs[:30]:
    print(img)

# Find creature blocks
for h in soup.find_all(["h1", "h2", "h3", "h4"]):
    print(h.text.strip())
