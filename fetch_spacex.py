import requests
import os


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
    response_data = response.json()
    image_links = response_data['links']['flickr_images']

    for image_number, image_url in enumerate(image_links):
        file_name = f'spacex{image_number}{get_filename_extension(image_url)}'
        download_file(url=image_url, file_name=file_name)


def get_filename_extension(file_name):
    _, extension  = os.path.splitext(file_name)
    return extension
    


if __name__ == "__main__":
    fetch_spacex_last_launch()
