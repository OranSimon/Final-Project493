from playwright.sync_api import sync_playwright
from util import generate_global_grid, encode_hash


URL = "https://showmystreet.com/#"
CANVAS_SELECTOR = "#pano_canvas > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(9) > div > div > canvas:nth-child(1)"
OVERLAPPING_SELECTORS = [
    "#lookaround",
    "#pano_canvas > div > div:nth-child(14) > div > a > div > img",
    "#ad",
    "#pano_canvas > div > div:nth-child(16) > div",
    "#pano_canvas > div > div:nth-child(2) > div:nth-child(1) > div.gmnoprint.SLHIdE-sv-links-control > svg",
]


def take_screenshots(coordinates, output_folder):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for i, (lat, lng) in enumerate(coordinates):
            hash_str = encode_hash(lat, lng, 147, 401, 0.7, 0, "6")
            print(hash_str.lower())
            page.goto(URL + hash_str.lower())
            page.wait_for_load_state("networkidle")

            for selector in OVERLAPPING_SELECTORS:
                page.evaluate(
                    f"document.querySelector('{selector}').style.display = 'none'"
                )

            element = page.query_selector(CANVAS_SELECTOR)
            if element:
                screenshot_filename = f"{output_folder}/screenshot_{i}_{lat}_{lng}.png"
                element.screenshot(path=screenshot_filename)
                print(
                    f"Element screenshot taken for coordinates ({lat}, {lng}) and saved as {screenshot_filename}"
                )
            else:
                print(f"Element not found for coordinates ({lat}, {lng})")

        browser.close()


if __name__ == "__main__":
    START_LAT = -40
    START_LNG = 100
    LAT_DIV = 10
    LNG_DIV = 20

    TEST_COORDINATES = [(30.399504, 105.165894)]

    coordinates = generate_global_grid(START_LAT, START_LNG, LAT_DIV, LNG_DIV)
    take_screenshots(TEST_COORDINATES, "images")
