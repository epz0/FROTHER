import os
import base64
from PIL import Image

def get_images64(f_path, ids):
    """Returns a list with the base64 images and a list with the ids.

    Args:
        f_path (string): path for the folder with the images.
        ids (list): list to receive the ids as strings.

    Returns:
        ls_img64: as list.
    """
    ls_img64 = []
    for i in range(len(ids)):
        image_path = os.path.join(f_path, f'{ids[i]}.png')

        with open(image_path, "rb") as imageFile:
            binaryData = imageFile.read()
            base64EncodedData = base64.b64encode(binaryData)
            ls_img64.append(base64EncodedData.decode('utf-8'))

    return ls_img64

def get_all_ids(f_path):
    ids = []

    for filename in os.listdir(f_path):
        imagePath = os.path.join(f_path, filename)
        ids.append(os.path.splitext(filename)[0])

    return ids