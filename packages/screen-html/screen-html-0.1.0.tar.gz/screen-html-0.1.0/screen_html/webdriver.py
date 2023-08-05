"""
This is a Python script that uses Playwright to render HTML and take screenshots of web pages.

:param html: The HTML content to be rendered and saved as a file
:param body: A dictionary containing variables to be passed to the Jinja2 template for rendering the
HTML file
"""

import os
import jinja2
from playwright.async_api import async_playwright


HTML_FILE = os.path.join(os.path.dirname(__file__), 'index.html')

WIDTH = 1920
HEIGHT = 1080
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
CHROME_ARGS = [
    '--headless',
    '--disable-gpu',
    '--disable-dev-shm-usage',
    '--no-sandbox',
    '--log-level=3',
    '--disable-extensions',
    '--disable-infobars',
    '--disable-notifications',
    '--disable-popup-blocking',
    '--disable-save-password-bubble',
    '--disable-translate',
    '--disable-web-security',
    '--incognito',
    '--mute-audio'
    # '--disable-image-loading'
]


async def render_html(html, body={}):
    if os.path.isfile(html):
        with open(html, 'r', encoding='utf-8') as f:
            html = f.read()

    template = jinja2.Template(html)
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(template.render(body))


async def screenshot(file=None, full_page=False, omit_background=True):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page()

        await page.set_viewport_size({
            'width': WIDTH,
            'height': HEIGHT
        })

        if file:
            await page.goto('file://' + HTML_FILE)

        return await page.screenshot(path=file, full_page=full_page, omit_background=omit_background)
