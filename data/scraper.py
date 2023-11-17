import asyncio
from playwright.async_api import async_playwright
from util import generate_coordinates, encode_hash

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
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        for lat, lng in coordinates:
            hash_str = encode_hash(lat, lng, 147, 401, 0.7, 0, "6")
            print(URL + hash_str.lower())
            await page.goto(URL + hash_str.lower())
            await page.wait_for_load_state("networkidle")

            # Hide overlapping elements
            for selector in OVERLAPPING_SELECTORS:
                await page.evaluate(
                    f"document.querySelector('{selector}').style.display = 'none'"
                )

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
    start_lat, start_lng = 40, -74  # Example start coordinates
    end_lat, end_lng = 41, -75  # Example end coordinates
    lat_divisions, lng_divisions = 2, 2  # Number of subdivisions

    coordinates = generate_coordinates(
        start_lat, start_lng, end_lat, end_lng, lat_divisions, lng_divisions
    )

    test_coords = [(38.726050, -100.608492)]

    await take_screenshots(test_coords, "images")


if __name__ == "__main__":
    asyncio.run(main())
