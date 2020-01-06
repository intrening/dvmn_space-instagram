import os
import argparse
from dotenv import load_dotenv
from PIL import Image
from instabot import Bot
from fetch_hubble import fetch_huble_images_from_collection
from fetch_spacex import fetch_spacex_last_launch


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


def public_photo_to_insta(insta_bot, image_path):
    insta_bot.upload_photo(image_path)


def public_photos(insta_bot, folder_name):
    for file_name in os.listdir(folder_name):
        if file_name != '.DS_Store':
            file_path = os.path.join(folder_name, file_name)
            crop_to_square(file_path=file_path)
            public_photo_to_insta(insta_bot=insta_bot, image_path=file_path)


def main():
    load_dotenv()
    insta_login = os.getenv("INSTA_LOGIN")
    insta_password = os.getenv("INSTA_PASSWORD")

    parser = argparse.ArgumentParser()
    parser.add_argument("collection")
    args = parser.parse_args()
    collection = args.collection

    insta_bot = Bot()
    insta_bot.login(username=insta_login, password=insta_password)

    fetch_spacex_last_launch()
    fetch_huble_images_from_collection(collection=collection)
    public_photos(insta_bot, 'media')


if __name__ == "__main__":
    main()