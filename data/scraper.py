import asyncio
from playwright.async_api import async_playwright
from util import generate_coordinates, encode_hash, generate_random_point_on_land
import geopandas as gpd

URL = "https://showmystreet.com/#"
CANVAS_SELECTOR = "#pano_canvas > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(9) > div > div > canvas:nth-child(1)"
OVERLAPPING_SELECTORS = [
    "#lookaround",
    "#pano_canvas > div > div:nth-child(14) > div > a > div > img",
    "#ad",
    "#pano_canvas > div > div:nth-child(16) > div",
    "#pano_canvas > div > div:nth-child(2) > div:nth-child(1) > div.gmnoprint.SLHIdE-sv-links-control > svg",
]


async def take_screenshots(coordinates, output_folder):
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()

        for lat, lng in coordinates:
            await page.goto(URL)
            await page.get_by_role("textbox").nth(0).click()
            await asyncio.sleep(0.5)
            await page.get_by_role("textbox").nth(1).type(str(lat) + "," + str(lng))
            await asyncio.sleep(0.5)
            await page.get_by_role("textbox").nth(0).click()
            await asyncio.sleep(0.5)
            await page.get_by_role("textbox").nth(0).press('Enter')
            await page.wait_for_load_state("networkidle")

            await page.locator("#up").dblclick()

            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(1)

            # Hide overlapping elements
            for selector in OVERLAPPING_SELECTORS:
                await page.evaluate(
                    f"document.querySelector('{selector}').style.display = 'none'"
                )

            await page.evaluate('(selector) => document.querySelector(selector).remove()', '#small')
            await page.evaluate('(selector) => document.querySelector(selector).remove()', '#zoomout')
            await page.evaluate('(selector) => document.querySelector(selector).remove()', '#zoomin')
            await page.evaluate('(selector) => document.querySelector(selector).remove()', '#ctlSplitter > div.handle')
            await page.evaluate('(selector) => document.querySelector(selector).remove()', '#searchinput')

            await page.wait_for_load_state("networkidle")


            # Take a screenshot of the target element
            element = await page.query_selector(CANVAS_SELECTOR)
            if element:
                screenshot_filename = f"{output_folder}/screenshot_{lat}_{lng}.png"
                await element.screenshot(path=screenshot_filename)
                print(
                    f"Screenshot taken for coordinates ({lat}, {lng}) and saved as {screenshot_filename}"
                )
            else:
                print(f"Element not found for coordinates ({lat}, {lng})")

            await page.close()
            page = await browser.new_page()

        await browser.close()


async def main():

    land = gpd.read_file("ne_50m_land.shp")
    random_point = []
    for i in range(100):
        random_point.append(generate_random_point_on_land(land))

    await take_screenshots(random_point, "images")



if __name__ == "__main__":
    asyncio.run(main())
