import os
import io
import time
import requests
import argparse
from PIL import Image
from base64 import b64decode
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def initialize():
    parser = argparse.ArgumentParser(description='A Python script for automated image scraping from Google Images, ideal for creating datasets for machine learning and AI projects')

    parser.add_argument('--output-path', help='Base path where images will be saved')
    parser.add_argument('--query-terms', nargs='+', help='Terms that will be used for search images. Accept multiple values')
    parser.add_argument('--pages', type=int, help='Quantity of pages to be fetched')

    return parser.parse_args()

def get_output_folder(base_output_path, query):
    folder_name = os.path.join(base_output_path + '/output', query)

    try:
        os.makedirs(folder_name)
    except Exception as e:
        print(f"Wasn't possible to create/access output folder for query '{query}'. Internal error: {str(e)}")

    return folder_name

def initialize_driver():
    options = FirefoxOptions()
    options.add_argument("--headless")
    return webdriver.Firefox(options=options)

def finalize_driver(driver):
    driver.quit()

def create_query_url(query):
    escaped_query = quote(query)
    return f"https://www.google.com/search?q={escaped_query}&tbm=isch"

def start_processing(base_output_path, query_terms, pages_quantity):
    print(f"Processing started.")

    driver = initialize_driver()

    for query in query_terms:
        search_and_download_images(driver, query, base_output_path, pages_quantity)
        time.sleep(10)

    print(f"Processing finished.")
    finalize_driver(driver)

def search_and_download_images(driver, query, base_output_path, pages_quantity):
    print(f"Searching images for query '{query}'...")

    driver.get(create_query_url(query))
    await_images_load(driver, pages_quantity)

    imgs_elements = get_images_elements(driver)
    output_path = get_output_folder(base_output_path, query)

    downloaded_images_count = download_images_elements(imgs_elements, output_path)

    print(f"Total of {downloaded_images_count} downloaded.")

def await_images_load(driver, pages_quantity):
    for _ in range(pages_quantity):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

def get_images_elements(driver):
    try:
        return driver.find_elements(By.CSS_SELECTOR,'img.rg_i')
    except Exception as e:
        print(f"Wasn't possible to get image elements from Google search results. Internal error: {str(e)}")

def download_images_elements(imgs_elements, output_path):
    downloaded_images_counter = 0

    for index, img in enumerate(imgs_elements):
        img_src = img.get_attribute("src")

        if not img_src:
            continue

        if img_src.startswith('http'):
            download_image_from_url(img_src, output_path, f"{index + 1}.jpg")
            downloaded_images_counter += 1
        elif img_src.startswith('data:image/jpeg;base64'):
            download_image_from_base64(img_src, output_path, f"{index + 1}.jpg")
            downloaded_images_counter += 1

    return downloaded_images_counter

def download_image_from_url(url, output_path, filename):
    img_response = requests.get(url)
    img_path = os.path.join(output_path, filename)

    with open(img_path, "wb") as img_file:
        img_file.write(img_response.content) 

def download_image_from_base64(base64, output_path, filename):
    img_data = base64.split('base64,')[1]
    img = Image.open(io.BytesIO(b64decode(img_data)))
    img_path = os.path.join(output_path, filename)
    img.save(img_path)

args = initialize()

start_processing(args.output_path, args.query_terms, args.pages)
