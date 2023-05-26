import requests


class YandexDisk:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_folder(self, user_id):
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
        print(f'Папка отсутствует, создаем...статус: {response.status_code}')

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        print(f'Получаем ссылку на загрузку: {response.status_code}')
        return response.json()

    def upload_file_to_disk(self, disk_file_path, url):
        href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
        response = requests.put(href, requests.get(url))
        response.raise_for_status()
        print(f'Статус загрузки: {response.status_code}')
        if response.status_code == 201:
            print("Success")
