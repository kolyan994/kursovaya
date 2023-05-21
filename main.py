import requests
import os
from dotenv import load_dotenv
from tqdm import tqdm
import json
from pprint import pprint

load_dotenv()
class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_folder(self,user_id):
        folder_url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        params = {'path': 'kursovaya/' + str(user_id)}
        response = requests.get(folder_url, headers=headers, params=params)
        return response.status_code

    def new_folder(self, user_id):
        folder_url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        params = {'path': 'kursovaya/' + str(user_id)}
        response = requests.put(folder_url, headers=headers, params=params)

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        print(response.status_code)
        pprint(response.json())
        return response.json()

    def upload_file_to_disk(self, disk_file_path, url):
        href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
        response = requests.put(href, requests.get(url))
        response.raise_for_status()
        print(response.status_code)
        if response.status_code == 201:
            print("Success")

class VkApiHandler:
    base_url = 'https://api.vk.com/method/'

    def __init__(self, access_token, version='5.131'):
        self.params = {
            'access_token': access_token,
            'v': version
        }


    def get_photo(self, owner_id):
        method_name = f'{self.base_url}photos.getAll'
        params = {'owner_id': owner_id, 'extended': 1, 'count': 100, **self.params}
        response = requests.get(method_name, params=params)
        data = response.json()
        users_photo = {}
        for photo in data['response']['items']:
            for size in photo['sizes']:
                if size['type'] == 'z':
                    photo_url = size['url']
            if photo['likes']['count'] not in users_photo:
                users_photo[photo['likes']['count']] = photo_url
            else:
                name = f'{photo["likes"]["count"]}+{photo["date"]}'
                users_photo[name] = photo_url
        return users_photo

#Вводим ID пользователя вконтакте
user_id = int(input('Введите ID пользователя Вконтакте'))
#Получаем токены и версию из .env файла
vk_token = os.getenv('VK_API_TOKEN')
version = os.getenv('VERSION')
ya_token = os.getenv('YA_TOKEN')
#объявляем переменные классов
vk = VkApiHandler(vk_token, version)
ya = YandexDisk(ya_token)
#Получаем все фотографии пользователя вконтакте, сохраняем в файл
users_photo = vk.get_photo(user_id)
#полученный файл сохраняем в json формате
with open("data_file.json", "w") as write_file:
    json.dump(users_photo, write_file)
#Проверяем наличие папки на яндекс диске с именем ID пользователя. Если ее нет - создаем.
status_folder = ya.get_folder(user_id)
if status_folder == 404:
    ya.new_folder(user_id)
#загружаем все фотографии на яндекс диск
for name, url in tqdm(users_photo.items()):
    path = f'kursovaya/{user_id}/{name}'
    ya.upload_file_to_disk(path, url)
