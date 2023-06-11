import requests
from pprint import *
import json
import os
import shutil

def course_work(vk_key, ya_token, vk_id=1, vk_version='5.131'):
    '''Скачивает фотографии и информацию о них из VK; загружает на Yandex.disk'''
    class YaUploader:
        def __init__(self, token: str):
            '''Инициализирует класс "YaUploader"'''
            self.token = token
        
        def get_headers(self):
            '''Получает заголовки для Yandex.disk'''
            return {'Content-Type': 'application/json', 'Authorization' : f'{self.token}'}
        
        def get_link(self, filename):
            '''Получает ссылку на загрузку файлов на Yandex.disk'''
            url_for_files = "https://cloud-api.yandex.net/v1/disk/resources/upload"
            headers = self.get_headers()
            params = {'path':file_list[number], 'overwrite':'true'}
            response = requests.get(url=url_for_files, headers=headers, params=params)
            link = response.json()
            return link['href']

        def upload(self, file_path: str):
            '''Загружает файлы на Yandex.disk'''
            url = 'https://cloud-api.yandex.net/v1/disk/resourses/publish'
            href = self.get_link(file_path)
            response = requests.put(href, open(f'{os.getcwd()}/photos/{file_path}', 'rb'))


    class VK: 
        def __init__(self, token, version):
            '''Инициализирует класс "VK"'''
            self.params = {'access_token':token, 'v':version, 'owner_id': vk_id, 'album_id': 'profile', 'extended': 1}

        def get_photo(self):
            '''Получает фотографии из профиля VK'''
            print('Getting photos has started')
            photo_url = 'https://api.vk.com/method/' + 'photos.get'
            params = self.params
            photos = requests.get(photo_url, params)
            response = photos.json()['response']['items'][:5]
            number_of_photos = len(response)
            link_list = []
            json_dict = {}
            for index in response:
                sizes = index['sizes']
                current_photo = 0
                resolution = 0
                for value in sizes:
                    current_resolution = value['height'] * value['width']
                    if current_resolution >= resolution:
                        resolution = current_resolution
                        current_photo = value
                        download_url = current_photo['url']
                link_list.append(download_url)
            doubles_check = []
            for value in range(len(link_list)):
                doubles_check.append(response[value]["likes"]["count"])
            if len(set(doubles_check)) == len(doubles_check):
                for value in range(len(link_list)):
                    with open(f'photos/{response[value]["likes"]["count"]}_likes.jpg', 'wb') as photo_for_download:
                        photo_for_download.write(requests.get(link_list[value]).content)
                print('Getting photos has been complited')
            else:
                for value in range(len(link_list)):
                    with open(f'photos/{response[value]["likes"]["count"]}_likes_{response[value]["date"]}_date.jpg', 'wb') as photo_for_download:
                        photo_for_download.write(requests.get(link_list[value]).content)
                print('Getting photos has been complited')
        
        def get_info(self):
            '''Получает информацию о фотографиях из профиля VK'''
            print('Getting info has started')
            photo_url = 'https://api.vk.com/method/' + 'photos.get'
            params = self.params
            photos = requests.get(photo_url, params)
            response = photos.json()['response']['items'][:5]
            number_of_photos = len(response)
            link_list = []
            json_dict = {}
            for id, index in enumerate(response):
                sizes = index['sizes']
                current_photo = 0
                resolution = 0
                for value in sizes:
                    current_resolution = value['height'] * value['width']
                    if current_resolution >= resolution:
                        resolution = current_resolution
                        current_photo = value
                        download_url = current_photo['url']
                json_dict[f'file_{id+1}'] = {"file_name" : f'{response[id]["likes"]["count"]}_likes.jpg', 'size' : current_photo['type']}
            with open(f'photos/info.json', 'w') as info:
                json.dump(json_dict, info)
            print('Getting info has been complited')

    print('Compliting the task has started')
    user = VK(vk_key, vk_version)
    if os.path.isdir('photos'):
        shutil.rmtree(f"{os.getcwd()}/photos")
    os.mkdir('photos')
    user.get_photo()
    user.get_info()
    file_list = os.listdir(f"{os.getcwd()}/photos")
    token = ya_token
    uploader = YaUploader(token)
    print('Uploading has started')
    for number in range(len(file_list)):    
        uploader.upload(file_list[number])
    print('Uploading has been finished')
    print('Compliting the task has been finished')

course_work('Введите токен VK вместо этой строки', "Введите токен Yandex вместо этой строки", 1, '5.131')