# Readme

## Описание

Есть папка [Yandex Disk](https://disk.yandex.ru/d/V47MEP5hZ3U1kg). Требуется написать код, который по запросу из списка папок, собирает картинки из этих папок в один TIFF файл.

Выполненено на Python.
## Пример

На входе список: `['1388_12_Наклейки 3-D_3']`

На выходе файл: `combined_image.tif`

## Требования

- Python 3.8+
- [Google Chrome](https://www.google.com/chrome/)
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
- Установленные библиотеки Python (см. ниже)

## Установка


1. Создайте виртуальное окружение и активируйте его:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`
    ```

2. Установите необходимые зависимости:

    ```bash
    pip install -r requirements.txt
    ```

3. Создайте файл `.env` в корне проекта и добавьте следующие переменные окружения:

    ```env
    FOLDER_URL=https://example.com/folder/
    CHROME_DRIVER_PATH=/path/to/chromedriver
    ```

    - `FOLDER_URL` - базовый URL, где находятся папки с изображениями.
    - `CHROME_DRIVER_PATH` - путь к вашему ChromeDriver.

## Использование

1. Запустите скрипт для загрузки изображений и их объединения в TIF файл:

    ```bash
    python create_file.py
    ```
