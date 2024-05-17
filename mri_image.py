from enum import Enum
import pydicom
import numpy as np


class MriTags(Enum):
    IMG_POS = (0x0020, 0x0032)
    IMG_ORI = (0x0020, 0x0037)
    PIXEL_SPACING = (0x0028, 0x0030)


class MriImage(object):

    def __init__(self, dicom_path=None, dicom_dataset=None):

        if dicom_dataset is None:
            if dicom_path is None:
                raise Exception("One arg must be populated.")
            dicom_dataset = pydicom.dcmread(dicom_path)

        self.ds = dicom_dataset

        self.img_pos = self.get(MriTags.IMG_POS)
        self.img_ori = self.get(MriTags.IMG_ORI)
        self.pixel_spacing = self.get(MriTags.PIXEL_SPACING)
        self.mat = self.transform_mat()

    def get(self, tag: MriTags):
        val = self.ds.get(tag.value)
        return tuple(float(x) for x in val)

    def tranform_pix(self, i, j):
        v = np.transpose([i, j, 0, 1])
        return np.matmul(self.mat, v)[:3]

    def transform_mat(self):
        """
        https://dicom.innolitics.com/ciods/ct-image/image-plane/00200037
        Equation C.7.6.2.1-1.
        """
        S = self.img_pos
        X = self.img_ori[:3]
        Y = self.img_ori[3:]
        Di, Dj = self.pixel_spacing

        mat = [
            [X[0] * Di, Y[0] * Dj, 0, S[0]],
            [X[1] * Di, Y[1] * Dj, 0, S[1]],
            [X[2] * Di, Y[2] * Dj, 0, S[2]],
            [0, 0, 0, 1],
        ]

        return np.array(mat)
