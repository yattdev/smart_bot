#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import time
import hashlib
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService


def show_notification(title, message):
    subprocess.run(['notify-send', f'{title} {message}'])

def get_page_content(driver, url, class_selector):
    # Open the website
    driver.get(url)
    # Wait for the page to load (you can adjust the sleep time as needed)
    time.sleep(5)

    # Find the elements using the specified CSS selector
    current_articles = driver.find_element(
        By.CLASS_NAME, class_selector
    )
    return current_articles.text

def hash_content(content):
    return hashlib.md5(content.encode()).hexdigest()

def check_for_new_articles(base_url, path, selector):
    url = f"{base_url}/{path}"
    try:
        # Configure the Chrome web driver
        chrome_path = "/usr/bin/chromedriver"
        chrome_service = ChromeService(chrome_path)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(
            service=chrome_service,
            options=options,
        )

        page_content = get_page_content(driver, url, class_selector)

        if not page_content:
            print(f"Failed to retrieve page content for {url}.")
            return

        content_hash = hash_content(page_content)

        if content_hash:
            hash_file_path = f"hash_{path.replace('/', '_')}.txt"

            if os.path.exists(hash_file_path):
                with open(hash_file_path, "r") as hash_file:
                    stored_hash = hash_file.read()

                if content_hash == stored_hash:
                    pass  # No new mission detected
                else:
                    show_notification("FREELANCE.MA",
                                      "!!! New freelance missions published !!!")

                # Update the stored hash
                with open(hash_file_path, "w") as hash_file:
                    hash_file.write(content_hash)
            else:
                # First run, save the hash
                with open(hash_file_path, "w") as hash_file:
                    hash_file.write(content_hash)
                    print(f"Initial hash saved for specific content in {path}.")
        else:
            print(f"Failed to hash specific content for {url}.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser window
        driver.quit()

if __name__ == "__main__":
    base_url = "https://www.freelancer.ma"
    specific_path = "missions"
    class_selector = "missions-freelance"  # Replace with the CSS selector for the specific content you want to hash
    check_for_new_articles(base_url, specific_path, class_selector)

