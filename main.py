import os
from dotenv import load_dotenv
from tqdm import tqdm
import json
from vk import VkApiHandler
from yandex import YandexDisk

load_dotenv()


def get_photo_information(data):
    users_photo = {}
    my_json = []
    temp_size = ''
    for photo in data['response']['items']:
        for size in photo['sizes']:
            if size['type'] == 'z':
                photo_url = size['url']
                temp_size = 'z'
            elif size['type'] == 'y':
                photo_url = size['url']
                temp_size = 'y'
            elif size['type'] == 'x':
                photo_url = size['url']
                temp_size = 'x'

        if photo['likes']['count'] not in users_photo:
            users_photo[photo['likes']['count']] = photo_url
            my_json.append({
                'file_name': f"{photo['likes']['count']}.jpg",
                'size': temp_size})
        else:
            name = f'{photo["likes"]["count"]}+{photo["date"]}'
            users_photo[name] = photo_url
            my_json.append({
                'file_name': f"{name}.jpg",
                'size': temp_size})
    return users_photo, my_json


# Вводим ID пользователя вконтакте и яндекс токен
user_id = int(input('Введите ID пользователя Вконтакте'))
ya_token = input('Введите токен яндекса')
# Получаем токены и версию vk api из .env файла
vk_token = os.getenv('VK_API_TOKEN')
version = os.getenv('VERSION')
# объявляем переменные классов
vk = VkApiHandler(vk_token, version)
ya = YandexDisk(ya_token)
# Получаем все фотографии пользователя вконтакте, сохраняем в файл
users_photo, my_json = get_photo_information(vk.get_photo(user_id))

# полученный файл сохраняем в json формате
with open("data_file.json", "w") as write_file:
    json.dump(my_json, write_file)
# Проверяем наличие папки на яндекс диске с именем ID пользователя. Если ее нет - создаем.
status_folder = ya.get_folder(user_id)
print(f'Статус проверки папки: {status_folder}')
if status_folder == 404:
    ya.new_folder(user_id)
# загружаем все фотографии на яндекс диск
for name, url in tqdm(users_photo.items()):
    path = f'kursovaya/{user_id}/{name}'
    ya.upload_file_to_disk(path, url)
