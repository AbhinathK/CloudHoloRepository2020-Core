import logging

import nibabel as nib
import numpy as np

from pipelines.adapters.dicom_file import read_dicom_as_np_ndarray_and_normalise
from pipelines.services.marching_cubes import generate_obj
from pipelines.adapters.nifty_file import normalise_nifti
from pipelines.wrappers.obj2gltf import call_obj2gltf


def convert_dicom_to_nifty(dicomInputPath, niftiOutputPath):
    # convert series of dicom to numpy
    # TODO: Read vs. convert
    dicomNumpyList = read_dicom_as_np_ndarray_and_normalise(dicomInputPath)

    # convert numpy array to nifti image
    niftiImage = nib.Nifti1Image(dicomNumpyList, affine=np.eye(4))
    nib.save(niftiImage, niftiOutputPath)

    return niftiOutputPath


def convert_numpy_to_obj(input_data, main_threshold, output_path):
    generate_obj(input_data, main_threshold, output_path)
    logging.info("numpy2obj: done")
    return output_path


def convert_obj_to_glb(input_obj_path: str, output_glb_path: str, delete_original_obj: bool = True,
                       compress_glb: bool = False):
    return call_obj2gltf(input_obj_path, output_glb_path, delete_original_obj, compress_glb)


def convert_nifty_to_numpy_and_normalise(input_nifti_path):
    # https://github.com/nipy/nibabel/issues/626
    nib.Nifti1Header.quaternion_threshold = -1e-06

    img = nib.load(input_nifti_path)
    img = normalise_nifti(img)
    numpyList = np.array(img.dataobj)
    return numpyList
