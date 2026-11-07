const puppeteer = require('puppeteer-core');

async function testPuppeteer() {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36');

  console.log('Navigating to tracker...');
  const res = await page.goto('https://hunger-companion.com/tracker', { waitUntil: 'networkidle2', timeout: 30000 });
  console.log('Tracker HTTP status:', res.status());
  console.log('Page title:', await page.title());

  // Test executing in page context
  const evalResult = await page.evaluate(async () => {
    return {
      hungerProgress: typeof window.HungerProgress,
      hungerTracker: typeof window.HUNGER_TRACKER,
      cookies: document.cookie,
      url: window.location.href
    };
  });
  console.log('Eval result:', evalResult);

  await browser.close();
}

testPuppeteer().catch(console.error);
