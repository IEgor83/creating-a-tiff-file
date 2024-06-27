import math
import os
import asyncio
import time
from io import BytesIO
from dotenv import load_dotenv
import aiohttp
from PIL import Image
from bs4 import BeautifulSoup
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем URL папки и путь к драйверу Chrome из переменных окружения
FOLDER_URL = os.getenv('FOLDER_URL')
CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH')


async def get_page(url):
    """Асинхронная функция для получения HTML-страницы с помощью Selenium (Selenium выбран, чтобы решать капчи,
    если они возникнут)"""
    webdriver_path = CHROME_DRIVER_PATH

    service = Service(webdriver_path)
    service.start()

    options = Options()
    options.headless = True

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(quote(url, safe=':/').replace('%D0%B8%CC%86', '%D0%B9'))

    #time.sleep(20)

    html = driver.page_source

    driver.quit()

    return html


async def fetch_image(session, url):
    """Асинхронная функция для загрузки изображения по URL"""
    async with session.get(url) as response:
        if response.status == 200:
            img_content = await response.read()
            img = Image.open(BytesIO(img_content))
            return img
        else:
            print(f"Failed to download image from {url} with status {response.status}")
            return None


async def download_images_async(folder_list):
    """Асинхронная функция для скачивания изображений из списка папок"""
    tasks = []

    for folder in folder_list:
        folder_url = FOLDER_URL + folder
        tasks.append(get_page(folder_url))

    html_responses = await asyncio.gather(*tasks)

    async with aiohttp.ClientSession() as session:
        image_tasks = []
        for html in html_responses:
            soup = BeautifulSoup(html, 'html.parser')
            image_tags = soup.find_all('img', class_='scalable-preview__image')
            image_urls = [img['src'] for img in image_tags if 'src' in img.attrs]

            print(f"Found {len(image_urls)} images in {html_responses.index(html)} response")

            for url in image_urls:
                image_tasks.append(fetch_image(session, url))

        # Запускаем все задачи загрузки изображений параллельно
        images = await asyncio.gather(*image_tasks)
        images = [img for img in images if img is not None]

    return images


def save_as_tiff(images):
    """Функция для сохранения списка изображений в файл TIFF"""
    if images:
        num_images = len(images)

        def find_best_grid(num):
            factors = [(i, num // i) for i in range(1, int(math.sqrt(num)) + 1) if num % i == 0]
            return min(factors, key=lambda x: abs(x[0] - x[1]))

        num_rows, num_cols = find_best_grid(num_images)

        img_width, img_height = images[0].size

        # Определение общей ширины и высоты итогового изображения
        total_width = img_width * num_cols
        total_height = img_height * num_rows

        # Создание нового изображения с определенными размерами
        combined_image = Image.new('RGB', (total_width, total_height))

        # Вставка всех изображений в новое изображение
        for i, img in enumerate(images):
            row = i // num_cols
            col = i % num_cols
            x_offset = col * img_width
            y_offset = row * img_height
            combined_image.paste(img, (x_offset, y_offset))

        # Сохранение итогового изображения в формате TIFF
        combined_image.save('combined_image.tif', format='TIFF')
        combined_image.show()
    else:
        print("No images to save")


if __name__ == '__main__':
    folder_list = ['1369_12_Наклейки 3-D_3']
    loop = asyncio.get_event_loop()
    images = loop.run_until_complete(download_images_async(folder_list))
    save_as_tiff(images)
