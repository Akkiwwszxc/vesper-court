"""Снимает каждую квартиру из 3D для Higgsfield: shots/f{этаж}-{номер}.jpg.

Запуск из корня проекта:
    python3 -m http.server 8000 &
    pip install playwright && playwright install chromium
    python3 tools/make_shots.py
"""
import asyncio, os
from playwright.async_api import async_playwright

URL = os.environ.get('URL', 'http://localhost:8000/index.html')
FLOORS, HOMES = 5, 4  # этажей и квартир на этаже

async def main():
    os.makedirs('shots', exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
        page = await (await browser.new_context(viewport={'width': 1600, 'height': 1000})).new_page()
        await page.goto(URL + '#shot-1-0')
        await page.wait_for_timeout(7000)
        for f in range(1, FLOORS + 1):
            for k in range(HOMES):
                await page.evaluate(f"location.hash='#shot-{f}-{k}'")
                await page.wait_for_timeout(2200)
                await page.screenshot(path=f'shots/f{f}-{k}.jpg', type='jpeg', quality=84)
        await browser.close()

asyncio.run(main())
