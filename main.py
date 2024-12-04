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
    def __init__(self, access_token, version = 5.199 ):
        self.access_token = access_token
        self.version = version
        self.base_drees = 'https://api.vk.com/method/'
        self.params = {'access_token': self.access_token,
                        'extended': 1,
                        'v': self.version}

    def get_photos(self,user_ids):

        url = f'{self.base_drees}photos.getAll'
        params = {'user_id': user_ids}
        params.update(self.params)
        responses = requests.get(url, params=params)

        if 200 <= responses.status_code < 300:
            items = responses.json()['response']['items']
            urls = [item['orig_photo']['url'] for item in items]
            likes = [item['likes']['count'] for item in items]
            result = dict(zip(likes,urls))
            return result

        else:
            return 'I think that your problem (token)'

    def check_token(self):
        url = f'{self.base_drees}account.getProfileInfo'
        response = requests.get(url, params=self.params)
        return response.json()

class YA_Push_Photo:
    def __init__ (self, result: dict, yandex_token, file_name: str):
        self.yandex_token = yandex_token
        self.base_drees_YA = 'https://cloud-api.yandex.net/v1/disk/resources'
        self.upload_file = result
        self.file_name = file_name

    def create_path(self):
        headers = {
            'Authorization': self.yandex_token
        }
        url = f'{self.base_drees_YA}'
        params = {
                  'path': self.file_name
                  }
        responses = requests.put(url, headers=headers, params=params)
        if responses.status_code == 409:
            return 'already created'
        else:
            return responses.json()

    def put_yandex(self):
        headers = {
            'Authorization': self.yandex_token
        }
        url = f'{self.base_drees_YA}/upload'
        params = {'path': 'API_VK.jpg/Photo1',
                 'url': 'https://sun9-11.userapi.com/s/v1/ig2/MXPIGCZXojervq7InLzroI1GGlcZG9mRbBynJbEAOwT-reGAqBx6eykVHsxvS7lqmLglU7RdBY3fwngYLzA2gGA0.jpg?quality=95&as=32x43,48x64,72x96,108x144,160x213,240x320,360x480,480x640,540x720,640x853,720x960,1080x1440,1280x1707,1440x1920,1920x2560&from=bu',
                  'disable_redirects': False
                  }
        responses = requests.post(url, headers=headers, params=params)
        return responses.json()


iVk = Vkontakte_all_photo(access_token)
token_check = iVk.check_token()
Im_check_man = iVk.get_photos(user_id)
iYA = YA_Push_Photo(Im_check_man,yandex_token,'API_VK.jpg')
YA_check = iYA.put_yandex()
Creater_path = iYA.create_path()
print(Creater_path)
print(YA_check)
# print(token_check)
#pprint(Im_check_man)
