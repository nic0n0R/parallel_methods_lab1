import re
import threading

import utils
import zipfile
import requests
import os
from bs4 import BeautifulSoup


def read_data(path: str) -> list:
    with open(path, 'r') as f:
        return f.readlines()


def download_data(url: str):
    try:
        print(f"Start downloading: {url}")
        response = requests.get(url)
        print(f"Download complete: {url}")
        return response
    except Exception as e:
        print(f"Error: {e=}")
        return None


def parse(content):
    hrefs_to_img = list()
    for c in content:
        if content is not None:
            soup = BeautifulSoup(str(c), "html.parser")
            a_tags = soup.find_all('a')
            for a in a_tags:
                images = a.find_all('img')
                hrefs = [image.get('src') for image in images]
                pattern = r"\.(jpg|jpeg|png|gif|bmp|svg|webp|ico)$"
                for img in hrefs:
                    if img is not None and img != "" and re.search(pattern, img):
                        hrefs_to_img.append(img)

    if len(hrefs_to_img) == 0:
        print("No hyperlinks in the provided sites")
    else:
        dir_to_save = "images"
        if not os.path.isdir(dir_to_save):
            os.makedirs(dir_to_save, exist_ok=True)
            print("Downloading images...")
        threads_downloading_images = list()
        for href in hrefs_to_img:
            thread = utils.MyThread(target=download_image, args=(href, dir_to_save,))
            threads_downloading_images.append(thread)
            thread.start()
        paths_to_downloaded_images = list()
        for t in threads_downloading_images:
            paths_to_downloaded_images.append(t.join())

        print("Done.")

        zipImages("images.zip", paths_to_downloaded_images)


def zipImages(archive_name, paths):
    print("Adding images to archive...")
    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as archive:
        for file in paths:
            archive.write(file, os.path.basename(file))
    print("Done")


def download_image(href_image, folder):
    try:
        response = requests.get(href_image)
        file_name = os.path.basename(href_image).strip()
        full_path = f"{folder}/{file_name}"
        with open(full_path, 'wb') as f:
            f.write(response.content)
        return full_path
    except:
        pass


def main():
    urls_path = "urls.txt"
    urls = read_data(urls_path)

    download_threads_by_urls = list()

    for url in urls:
        thread = utils.MyThread(target=download_data, args=(url,))
        download_threads_by_urls.append(thread)
        thread.start()
    result_downloading = list()

    for t in download_threads_by_urls:
        result_downloading.append(t.join())

    thread_parsing_content = threading.Thread(target=parse, args=(result_downloading,))
    thread_parsing_content.start()
    thread_parsing_content.join()
    print("Program end")


if __name__ == '__main__':
    main()



