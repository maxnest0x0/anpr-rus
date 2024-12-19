import requests
from bs4 import BeautifulSoup as BS
import os
from requests.exceptions import RequestException
import time


class ImageDownloader:
    def __init__(self, base_url="https://migalki.net/images.php", dataset_path="Dataset/Imgs",
                 num_images_to_download=10 ** 4, log_filename="A/nums.txt"):
        self.base_url = base_url
        self.dataset_path = dataset_path
        self.num_images_to_download = num_images_to_download
        self.log_filename = log_filename
        self.image_urls = set()
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"}

    def download_image(self, image_url, filename):

        try:
            response = requests.get(image_url[0], stream=True, headers=self.headers)
            response.raise_for_status()

            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            with open(self.log_filename, 'a') as f:
                f.write(image_url[1] + '\n')
            print(f"Изображение '{filename}' успешно скачано.")
            return True

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP ошибка при скачивании изображения: {http_err}")
            return False
        except RequestException as e:
            print(f"Ошибка при скачивании изображения: {e}")
            return False
        except OSError as os_err:
            print(f"Ошибка системы при сохранении файла: {os_err}")
            return False

    def _extract_image_urls(self, soup):

        blocks = soup.find_all('div', class_='col-xs-4')
        for block in blocks:
            imgs_url = block.find_all('img')
            if len(imgs_url) == 2:
                num = imgs_url[1].get('src')
                filename = os.path.splitext(os.path.basename(num))[0]
                big_img = block.find('a', class_='btn btn-success').get('href')
                self.image_urls.add((big_img, filename))
        return len(self.image_urls)

    def collect_image_urls(self):

        count = 0
        flag = True
        while flag:
            r = requests.get(f"{self.base_url}?start={count}", headers=self.headers)
            soup = BS(r.text, 'html.parser')
            num_images_collected = self._extract_image_urls(soup)
            print(f"Collected {num_images_collected} images so far")
            if num_images_collected >= self.num_images_to_download:
                flag = False
            count += 18

    def start_downloading(self):

        i = 0
        for img in self.image_urls:
            if self.download_image(img, f"{self.dataset_path}/{i}.jpg"):
                i += 1
            time.sleep(1)


if __name__ == "__main__":

    if not os.path.exists("Dataset/Imgs"):
        os.makedirs("Dataset/Imgs")

    if not os.path.exists("A"):
        os.makedirs("A")

    downloader = ImageDownloader(num_images_to_download=100)

    downloader.collect_image_urls()

    downloader.start_downloading()
