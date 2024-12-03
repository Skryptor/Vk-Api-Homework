import configparser
from http.client import responses

import requests
from pprint import pprint
config = configparser.ConfigParser()
config.read('settings.ini')
access_token = config["Tokens"]['access_token']
user_id = config["Tokens"]['user_id']
yandex_token = config["Tokens"]['yandex_token']
print(len(access_token))

class Vkontakte_all_photo:
    def __init__(self, access_token, yandex_token, version = 5.199 ):
        self.access_token = access_token
        self.yandex_token = yandex_token
        self.version = version
        self.base_drees = 'https://api.vk.com/method/'
        self.base_drees_YA = 'https://cloud-api.yandex.net/v1/disk/resources'
        self.params = {'access_token': self.access_token,
                        'extended': 1,
                        'v': self.version}

    def get_photos(self,user_ids):
        url = f'{self.base_drees}photos.getAll'
        params = {'user_id': user_ids}
        params.update(self.params)
        responses = requests.get(url, params=params)
        items = responses.json()['response']['items']
        urls = [item['orig_photo']['url'] for item in items]
        likes = [item['likes']['count'] for item in items]
        result = dict(zip(urls,likes))
        return result

    def check_token(self):
        url = f'{self.base_drees}account.getProfileInfo'
        response = requests.get(url, params=self.params)
        return response.json()




iVk = Vkontakte_all_photo(access_token, yandex_token)
token_check = iVk.check_token()
Im_check_man = iVk.get_photos(user_id)
#print(token_check)
pprint(Im_check_man)
