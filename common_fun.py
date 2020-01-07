import requests
import os

def get_filename_extension(file_name):
    _, extension  = os.path.splitext(file_name)
    return extension

def download_file(url, file_name):
    response = requests.request(method='get', url=url, verify=False)
    response.raise_for_status()

    folder_name = 'media'
    os.makedirs(folder_name, exist_ok=True)
    with open(os.path.join(folder_name, file_name), 'wb') as file:
        file.write(response.content)

