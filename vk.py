import requests


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
        return data
