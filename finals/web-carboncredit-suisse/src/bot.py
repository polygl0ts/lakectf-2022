async def visit(instance):
    from pyppeteer import launch
    import asyncio
    import os

    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    url = f"http://carboncredit-suisse:8000/{instance}/"
    print("Visiting", url)
    browser = await launch({"args": ["--no-sandbox", "--disable-setuid-sandbox"]})
    for _ in range(2):
        await asyncio.sleep(30)
        page = await browser.newPage()
        await page.goto(url)
        await page.click("#login")
        await page.type("#login_username", "admin")
        await page.type("#login_password", ADMIN_PASSWORD)
        await page.click("#login_submit")

    print("Time's up, destroying challenge!")
    await page.goto(url)
    await page.click("#login")
    await page.type("#login_username", "admin")
    await page.type("#login_password", ADMIN_PASSWORD)
    await page.click("#login_submit")
    await asyncio.sleep(1)
    await page.click("#dashboard_destroy")
    await browser.close()
