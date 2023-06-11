from tqdm import tqdm

import requests
import json


class VkApiHandler:
    data_foto = {}

    def __int__(self, access_token, version='5.131'):
        """Метод для получения токена ВК, и версии приложения"""
        self.params = {
            'access_token': access_token,
            'v': version
        }

    def get_user_foto(self, count=5):
        """Метод для получения основных параметров для получения фотографий из ВК"""
        id_vk = input('Введите id пользователя:  ')
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': id_vk,
            'album_id': input('Введите название альбома для копирования(profile, wall, saved):  '),
            'extended': '1',
            'photo_sizes': '1',
            'count': count,
            'access_token': token_vk,
            'v': '5.131'
        }
        response = requests.get(url, params=params)
        data = response.json()
        # print(data)

        if 'error' in data:
            print('Альбома с таким названием у пользователя не обнаружено')
        else:
            for foto in data['response']['items']:
                if foto['likes']['count'] not in self.data_foto:
                    for f in foto['sizes']:
                        if f['type'] == 'z':
                            self.data_foto[f"{foto['likes']['count']}.jpg"] = f['url']
                else:
                    for f in foto['sizes']:
                        if f['type'] == 'z':
                            self.data_foto[foto['date']] = f['url']
            return self.data_foto


class YandexDisk:

    def __init__(self, token_yd, path=input('Введите имя новой папки:  ')):
        """Метод для получения основных параметров для загрузки фотографий на ЯД"""
        self.token = token_yd
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }
        self.path = path

    def create_folder(self):
        """Создание папки на ЯД"""
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        response = requests.put(f'{url}?path={self.path}', headers=self.headers)
        if response.status_code == 201:
            print(f'Папка {self.path} создана')
        elif response.status_code == 409:
            print(f'Папка с именем {self.path} уже существует')

    def upload_file_to_disk(self):
        """Метод для загрузки фотографий на ЯД и получения json файла с информацией"""

        info = []

        for foto in tqdm(vk.data_foto.items()):
            upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
            params = {"path": f'{self.path}/{foto[0]}', "url": foto[1], "overwrite": "false"}
            response = requests.post(upload_url, headers=self.headers, params=params)

            # print(response.status_code)

            if response.status_code == 202:
                info.append({'file_name': str(foto[0]),
                             'size': 'z'
                             })
                # print(f"Резервное копирование {foto[0]} завершено")
        with open('info.json', 'w') as outfile:
            json.dump(info, outfile)
        # print(info)


if __name__ == '__main__':
    with open('tokenVK.txt', 'r') as token_file:
        token_vk = token_file.readline()

    vk = VkApiHandler()

    data = vk.get_user_foto(10)

    yd = YandexDisk(input('Введите токен с Полигона Яндекс.Диска:  '))
    create_folder = yd.create_folder()
    upload = yd.upload_file_to_disk()
