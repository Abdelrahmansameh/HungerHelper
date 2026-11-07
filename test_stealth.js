const puppeteer = require('puppeteer-core');

async function testStealth() {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: false, // Or we can test with headless or custom args
    ignoreDefaultArgs: ['--enable-automation'],
    args: [
      '--no-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--window-size=1280,800'
    ]
  });
  const page = await browser.newPage();
  await page.evaluateOnNewDocument(() => {
    delete Object.getPrototypeOf(navigator).webdriver;
  });
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36');

  console.log('Navigating...');
  const res = await page.goto('https://hunger-companion.com/tracker', { waitUntil: 'networkidle2', timeout: 30000 });
  console.log('Status:', res.status(), 'Title:', await page.title());

  await new Promise(r => setTimeout(r, 4000));
  console.log('After 4s Title:', await page.title());

  const evalResult = await page.evaluate(() => {
    return {
      title: document.title,
      hungerTracker: typeof window.HUNGER_TRACKER,
      questsLength: document.querySelectorAll('.quest, [data-slug]').length
    };
  });
  console.log('Eval:', evalResult);

  await browser.close();
}

testStealth().catch(console.error);
