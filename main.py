import configparser
#from http.client import responses
from tqdm import tqdm
import requests
#from pprint import pprint
config = configparser.ConfigParser()
config.read('settings.ini')
access_token = config["Tokens"]['access_token']
yandex_token = config["Tokens"]['yandex_token']
#print(len(access_token))

class VkontakteAllPhoto:
    def __init__(self, vk_token, version = 5.199 ):
        self.access_token = vk_token
        self.version = version
        self.base_drees = 'https://api.vk.com/method/'
        self.params = {'access_token': self.access_token,
                        'extended': 1,
                        'v': self.version}

    def get_photos(self, count = 10):

        url = f'{self.base_drees}photos.getAll'
        params = {'user_id': input('you user id  '),'count': count}
        params.update(self.params)
        responses = requests.get(url, params=params)

        if 200 <= responses.status_code < 300:
            items = responses.json()['response']['items']
            urls = [item['sizes'][-1]['url'] for item in items]
            likes = [item['likes']['count'] for item in items]
            result = dict(zip(likes, urls))
            return result
        else:
            return 'I think that your problem (token)'

    def check_token(self):
        url = f'{self.base_drees}account.getProfileInfo'
        response = requests.get(url, params=self.params)
        return response.json()

class YAPushPhoto:
    def __init__ (self, result: dict, ya_token, file_name: str):
        self.yandex_token = ya_token
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
        elif 200 <= responses.status_code < 300:
            return 'created'
        else:
            return responses.json()

    def put_yandex(self,dict_photo):
        headers = {
            'Authorization': self.yandex_token
        }
        url = f'{self.base_drees_YA}/upload'

        for key,values in tqdm(dict_photo.items(), desc="Uploading photos to Yandex.Disk"):
            if key < 50:
                params = {'path': 'API_VK.jpg/неизвестный пока',
                        'url': values,
                        'disable_redirects': False
                    }
                responses = requests.post(url, headers=headers, params=params)
            else:
                params = {'path': 'API_VK.jpg/уже лучше',
                          'url': values,
                          'disable_redirects': False
                          }
                responses = requests.post(url, headers=headers, params=params)
        if 200 <= responses.status_code <300:
            return 'uploaded'
        else:
            return 'daunloadet you'




iVk = VkontakteAllPhoto(access_token)
token_check = iVk.check_token()
Im_check_man = iVk.get_photos(count=5)
iYA = YAPushPhoto(Im_check_man,yandex_token,'API_VK.jpg')
YA_check = iYA.put_yandex(Im_check_man)
Created_path = iYA.create_path()
print(Created_path)
print(YA_check)
#print(token_check)
#pprint(Im_check_man)
