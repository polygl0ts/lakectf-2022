from pyppeteer import launch
import asyncio
import os

async def visit(path):
    browser = await launch({'args': ['--no-sandbox', '--disable-setuid-sandbox']})
    page = await browser.newPage()
    url = "http://web:8080/"
    await page.goto(url)
    await asyncio.sleep(1)
    await page.setCookie({'name':'adminToken','value':os.environ["adminToken"]})
    url = f'http://web:8080{path}'
    print("Visiting", url)
    await page.goto(url)
    await asyncio.sleep(60)
    await browser.close()