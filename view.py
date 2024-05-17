import matplotlib.pyplot as plt
import pydicom
import os
from pprint import pprint
from PIL import Image
import pandas as pd
import json

from mri_image import MriImage

IMAGES_ROOT = "MRI_FILES/IMAGES/"
RENDERED_ROOT = "MRI_FILES/RENDERED/"

IMG_POS_TAG = (0x0020, 0x0032)
IMG_ORI_TAG = (0x0020, 0x0037)


def im_path_2_df(im_path):
    # Open the image using PIL
    img = Image.open(im_path)

    # Convert the image to RGB mode if it's not already in that mode
    img = img.convert("RGB")

    # Get the image data as a list of RGB tuples
    img_data = list(img.getdata())

    # Convert the list of tuples into a Pandas DataFrame
    df = pd.DataFrame(img_data, columns=["R", "G", "B"])
    return df


def get_files(images_root=IMAGES_ROOT, rendered_root=RENDERED_ROOT, load_files=True):
    img_rendered_pairs = []
    for dirpath, _, fnames in os.walk(images_root):
        for fname in fnames:
            fpath = os.path.join(dirpath, fname)
            fpath = os.path.normpath(fpath)
            rendered_fname = fpath.replace("IMAGES", "RENDERED")
            rendered_fname = os.path.join(rendered_fname, fname + "_0.jpg")
            rendered_fname = os.path.normpath(rendered_fname)
            if os.path.isfile(rendered_fname):
                img_rendered_pairs.append((fpath, rendered_fname))

    if not load_files:
        return img_rendered_pairs

    loaded_pairs = []
    for ds_path, img_path in img_rendered_pairs:
        ds = pydicom.dcmread(ds_path)
        df = im_path_2_df(img_path)
        loaded_pairs.append((ds, df))
    return loaded_pairs


def imshow(ds_file):
    ds = pydicom.dcmread(ds_file)
    plt.imshow(ds.pixel_array, cmap=plt.cm.bone)


def full_info_load(images_root=IMAGES_ROOT, rendered_root=RENDERED_ROOT):
    file_paths = get_files(load_files=False)
    files = get_files()

    infos = []
    for (ds, img), (ds_path, img_path) in zip(files, file_paths):
        infos.append(
            {
                "img_path": os.path.realpath(img_path),
                "pos": [float(x) for x in ds[IMG_POS_TAG]],
                "ori": [float(x) for x in ds[IMG_ORI_TAG]][:3],
            }
        )
    return infos


files = get_files()
ds = files[0][0]
mri_ds = MriImage(dicom_dataset=ds)


infos = full_info_load()
with open("infos.json", "w") as f:
    json.dump(infos, f)
print()
