import requests
from fetch_spacex import (
    get_filename_extension, download_file
)

def fetch_huble_image(image_id):
    huble_url = f'http://hubblesite.org/api/v3/image/{image_id}'
    response = requests.request(method='get', url=huble_url)
    response.raise_for_status()
    response_data = response.json()
    image_files = response_data['image_files']
    image_urls = ['http:' + image['file_url'] for image in image_files]
    if not image_urls:
        return False

    last_image_url = image_urls[-1]
    file_extention = get_filename_extension(file_name=last_image_url)
    file_name = f'huble_{image_id}{file_extention}'

    download_file(url=last_image_url, file_name=file_name)


def fetch_huble_images_from_collection(collection):
    url = f'http://hubblesite.org/api/v3/images/{collection}'
    response = requests.request(method='get', url=url)
    response.raise_for_status()
    response_data = response.json()
    image_ids = [image['id'] for image in response_data]
    for image_id in image_ids:
        fetch_huble_image(image_id=image_id)

