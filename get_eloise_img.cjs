const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

async function getEloise() {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: "new",
    args: ['--no-sandbox', '--disable-blink-features=AutomationControlled']
  });
  const page = await browser.newPage();
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36');

  console.log('Fetching Eloise page...');
  await page.goto('https://hunger-companion.com/npcs/eloise', { waitUntil: 'networkidle2', timeout: 20000 });
  
  // Find portrait image
  const imgSrc = await page.evaluate(() => {
    const imgs = Array.from(document.querySelectorAll('img'));
    for (const img of imgs) {
      if (img.src && (img.src.includes('eloise') || img.src.includes('npc') || img.src.includes('media'))) {
        return img.src;
      }
    }
    return imgs[0] ? imgs[0].src : null;
  });

  console.log('Found image src:', imgSrc);

  if (imgSrc) {
    const viewSource = await page.goto(imgSrc);
    const buffer = await viewSource.buffer();
    const outPath = path.resolve(__dirname, 'assets', 'eloise_avatar.png');
    fs.writeFileSync(outPath, buffer);
    console.log('Saved Eloise avatar to:', outPath);
  } else {
    // Take a screenshot of the main character card
    const outPath = path.resolve(__dirname, 'assets', 'eloise_avatar.png');
    await page.screenshot({ path: outPath, clip: { x: 50, y: 50, width: 300, height: 300 } });
    console.log('Saved Eloise screenshot to:', outPath);
  }

  await browser.close();
}

getEloise().catch(err => console.error('Puppeteer error:', err));
