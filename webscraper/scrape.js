// scrape.js
require('dotenv').config({ path: require('fs').existsSync('.env') ? '.env' : '../.env' });
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const url = require('url');
const axios = require('axios');

const TARGET_URL = process.env.TARGET_URL;
if (!TARGET_URL) {
  console.error('TARGET_URL not set in .env');
  process.exit(1);
}

const visited = new Set();
const downloadedPDFs = new Set();

function getDomainFolder(targetUrl) {
  const { hostname } = new url.URL(targetUrl);
  return hostname;
}

function sanitizeFilename(filename) {
  return filename.replace(/[^a-zA-Z0-9-_\.]/g, '_');
}

async function downloadFile(fileUrl, dest) {
  if (fs.existsSync(dest)) return;
  const writer = fs.createWriteStream(dest);
  const response = await axios({
    url: fileUrl,
    method: 'GET',
    responseType: 'stream',
  });
  response.data.pipe(writer);
  return new Promise((resolve, reject) => {
    writer.on('finish', resolve);
    writer.on('error', reject);
  });
}

async function scrapePage(page, pageUrl, domainFolder, pdfFolder) {
  if (visited.has(pageUrl)) return;
  visited.add(pageUrl);
  console.log('Visiting:', pageUrl);
  await page.goto(pageUrl, { waitUntil: 'networkidle2' });
  const html = await page.content();
  let filePath = 'index.html';
  if (pageUrl !== TARGET_URL) {
    const { pathname } = new url.URL(pageUrl);
    filePath = sanitizeFilename(pathname.endsWith('/') ? pathname.slice(1, -1) : pathname.slice(1)) || 'index.html';
    if (!filePath.endsWith('.html')) filePath += '.html';
  }
  const savePath = path.join(domainFolder, filePath);
  fs.mkdirSync(path.dirname(savePath), { recursive: true });
  fs.writeFileSync(savePath, html);

  // Find all links and pdfs
  const links = await page.$$eval('a', as => as.map(a => a.href));
  for (const link of links) {
    if (!link) continue;
    try {
      const parsed = new url.URL(link, pageUrl);
      if (parsed.hostname !== new url.URL(TARGET_URL).hostname) continue; // Stay in domain
      if (parsed.pathname.endsWith('.pdf')) {
        if (downloadedPDFs.has(parsed.href)) continue;
        downloadedPDFs.add(parsed.href);
        const pdfName = sanitizeFilename(path.basename(parsed.pathname));
        const pdfPath = path.join(pdfFolder, pdfName);
        fs.mkdirSync(pdfFolder, { recursive: true });
        console.log('Downloading PDF:', parsed.href);
        await downloadFile(parsed.href, pdfPath);
      } else if ((parsed.protocol === 'http:' || parsed.protocol === 'https:') && !visited.has(parsed.href)) {
        if (parsed.href.startsWith(TARGET_URL)) {
          await scrapePage(page, parsed.href, domainFolder, pdfFolder);
        }
      }
    } catch (e) {
      // Ignore invalid URLs
    }
  }
}

(async () => {
  const domainFolder = getDomainFolder(TARGET_URL);
  const pdfFolder = path.join(domainFolder, 'pdfs');
  fs.mkdirSync(domainFolder, { recursive: true });
  fs.mkdirSync(pdfFolder, { recursive: true });
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  try {
    await scrapePage(page, TARGET_URL, domainFolder, pdfFolder);
  } catch (err) {
    console.error('Error during scraping:', err);
  }
  await browser.close();
})(); 