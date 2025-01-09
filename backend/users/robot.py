import os
from time import sleep
from playwright.sync_api import sync_playwright


def check_profile_as_admin(uuid: str):
    sleep(5)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("http://localhost:5000/login")

        page.fill("input[name='username']", "admin")
        page.fill("input[name='password']", os.getenv("ADMIN_PASSWORD", "passord"))
        page.press("input[name='password']", "Enter")

        page.wait_for_url("http://localhost:5000/*", timeout=10000)

        try:
            page.goto(f"http://localhost:5000/profile/{uuid}", timeout=1000)
        except Exception:
            print('time out')

        browser.close()


if __name__ == "__main__":
    check_profile_as_admin("c18f9f88-033a-4243-bcb8-7ccfd99f08e9")
