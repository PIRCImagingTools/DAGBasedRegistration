from __future__ import print_function
import argparse
from nipy import load_image, save_image
from nipy.core.api import Image
import os
import numpy as np
from os import listdir
from os.path import isfile, join

# set up the argparse
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', help='Directory containing a series of timepoint .nii or .nii.gz images to combine into a single image',
                    required=True)
parser.add_argument('-o', '--out-image', help='Filename of the output image to write to (default directory is the input directory)',
                    default='', required=True)
parser.add_argument('-c', '--coordinate_image', help='Name of the image with the correct coordinate map', required=True)

# parse the args
args = parser.parse_args()
imgsDir = args.directory
outFn = args.out_image

# check that the directory exists
if not os.path.exists(imgsDir):
    raise IOError('Error: the specified directory does not exist')

# check that directory contains .nii or .nii.gz images
files = [join(imgsDir, f) for f in listdir(imgsDir) if isfile(join(imgsDir, f)) and (f.endswith('.nii.gz') or f.endswith('.nii'))]

# make the output file name
if outFn == '':
    outFn = imgsDir+outFn

# get the coordinates
img = load_image(args.coordinate_image)
coords = img.coordmap
print(coords)
print(img.shape)

# Now stack the images
imgs = []
for fn in files:
    img = load_image(fn)
    print(img.shape)
    if len(img.get_data().shape) == 4:
        imgs.append(np.squeeze(img.get_data()))
    else:
        imgs.append(img.get_data())

imgStack = np.stack(imgs, axis=-1)
print(imgStack.shape)
print(coords)

# and save the stacked image
registeredImg = Image(imgStack, coords)
save_image(registeredImg, outFn)

print('Nifti images merged to', outFn)
