import requests
import os
from os import listdir
from dotenv import load_dotenv
from PIL import Image
from instabot import Bot
from PIL import Image


def download_file(url, file_name):
    response = requests.request(method='get', url=url, verify=False)
    response.raise_for_status()

    folder_name = 'media'
    os.makedirs(folder_name, exist_ok=True)
    with open(os.path.join(folder_name, file_name), 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch():
    spacex_url = 'https://api.spacexdata.com/v3/launches/latest'
    response = requests.request(method='get', url=spacex_url)
    response.raise_for_status()
    json_content = response.json()
    image_links = json_content['links']['flickr_images']

    for image_number, image_url in enumerate(image_links):
        file_name = f'spacex{image_number}.{get_filename_extension(image_url)}'
        download_file(url=image_url, file_name=file_name)


def fetch_huble_image(image_id):
    huble_url = f'http://hubblesite.org/api/v3/image/{image_id}'
    response = requests.request(method='get', url=huble_url)
    response.raise_for_status()
    json_data = response.json()
    image_files = json_data['image_files']
    image_urls = ['http:' + image['file_url'] for image in image_files]
    if not image_urls:
        return False

    last_image_url = image_urls[-1]
    file_extention = get_filename_extension(file_name=last_image_url)
    file_name = f'huble_{image_id}.{file_extention}'

    download_file(url=last_image_url, file_name=file_name)


def get_filename_extension(file_name):
    return file_name.split('.')[-1]


def fetch_huble_images_from_collection(collection):
    url = f'http://hubblesite.org/api/v3/images/{collection}'
    response = requests.request(method='get', url=url)
    response.raise_for_status()
    json_data = response.json()
    image_ids = [image['id'] for image in json_data]
    for image_id in image_ids:
        fetch_huble_image(image_id=image_id)


def crop_to_square(file_path):
    image = Image.open(file_path)
    square_len = image.width if image.width < image.height else image.height
    width_move = (image.width - square_len) // 2
    height_move = (image.height - square_len) // 2

    coordinates = (
        width_move, height_move,
        image.width - width_move, image.height - height_move,
    )
    cropped = image.crop(coordinates)
    cropped.save(file_path)


def public_photo_to_insta(image_path):
    load_dotenv()
    insta_login = os.getenv("INSTA_LOGIN")
    insta_password = os.getenv("INSTA_PASSWORD")
    insta_bot = Bot()
    insta_bot.login(username=insta_login, password=insta_password)

    caption = image_path.replace("-", " ")

    insta_bot.upload_photo(image_path, caption=caption)
    if insta_bot.api.last_response.status_code != 200:
        print(insta_bot.api.last_response)


def public_photos(folder_name):
    for file_name in listdir(folder_name):
        print (file_name)


if __name__ == "__main__":
    # fetch_spacex_last_launch()
    # fetch_huble_images_from_collection(collection='spacecraft')
    # crop_to_square(file_path='/Users/nick/Documents/GitHub/dvmn_space-instagram/dvmn_space-instagram/media/huble_333.tif')
    # public_photo_to_insta(image_path='/Users/nick/Documents/GitHub/dvmn_space-instagram/dvmn_space-instagram/another.jpg')
    # public_photos(folder_name='media')
    pass