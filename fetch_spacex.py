import requests
from common_fun import (
    get_filename_extension, download_file
)


def fetch_spacex_last_launch():
    spacex_url = 'https://api.spacexdata.com/v3/launches/latest'
    response = requests.request(method='get', url=spacex_url)
    response.raise_for_status()
    response_data = response.json()
    image_links = response_data['links']['flickr_images']

    for image_number, image_url in enumerate(image_links):
        file_name = f'spacex{image_number}{get_filename_extension(image_url)}'
        download_file(url=image_url, file_name=file_name)


if __name__ == "__main__":
    fetch_spacex_last_launch()
