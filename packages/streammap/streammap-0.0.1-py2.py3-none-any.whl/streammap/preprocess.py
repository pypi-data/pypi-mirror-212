# -*- coding: utf-8 -*-

import numpy as np

def mndwi(green_band, mir_band):
    # Convert the bands to floating point data type
    green_band = green_band.astype(np.float32)
    mir_band = mir_band.astype(np.float32)

    # Calculate MNDWI
    mndwi = (green_band - mir_band) / (green_band + mir_band + 1e-8)

    return mndwi

# Apply contrast stretch to an input image
def contrastStretch(I):
    return (I - np.min(I)) / (np.max(I) - np.min(I))

# Convert image datatype to float
def im2double(I):
    if I.dtype == 'uint8':
        I = I.astype('float')/255
        
    if I.dtype == 'uint16':
        I = I.astype('float')/65535
    
    return I

# Convert double data array to image
def double2im(I, datatype):

    if datatype == 'uint8':
        I = I * 255
        
    if datatype == 'uint16':
        I = I * 65535

    return I.astype(datatype)
