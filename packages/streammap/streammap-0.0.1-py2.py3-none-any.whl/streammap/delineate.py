# -*- coding: utf-8 -*-

import cv2
import numpy as np
from scipy.ndimage import sum as ndsum
from scipy.ndimage import label as ndlabel
from streammap.modules import preprocess

# Uses the previously computed singularity index response (psi) and the dominant orientation (orient) to extract centerlines - Returns nms : Non-maxima suppressed singularity index response (centerlines).
def extractCenterlines(orient, psi):

    # Bin orientation values
    Q = ((orient + np.pi/2) * 4 / np.pi + 0.5).astype('int') % 4

    # Handle borders
    mask = np.zeros(psi.shape, dtype='bool')
    mask[1:-1, 1:-1] = True

    # Find maxima along local orientation
    nms = np.zeros(psi.shape)
    for q, (di, dj) in zip(list(range(4)), ((1, 0), (1, 1), (0, 1), (-1, 1))):
        for i, j in zip(*np.nonzero(np.logical_and(Q == q, mask))):
            if psi[i, j] > psi[i + di, j + dj] and psi[i, j] > psi[i - di, j - dj]:
                nms[i, j] = psi[i,j]

    return nms

# Uses a continuity-preserving hysteresis thresholding to classify centerlines.
def thresholdCenterlines(nms, tLow=0.012, tHigh=0.12, bimodal=True):

    if bimodal:
        #Otsu's algorithm
        nms = preprocess.double2im(nms, 'uint8')
        tHigh,_ = cv2.threshold(nms, nms.min(), nms.max(), cv2.THRESH_OTSU)
        tLow = tHigh * 0.1

    strongCenterline    = nms >= tHigh
    centerlineCandidate = nms >= tLow

    # Find connected components that has at least one strong centerline pixel
    strel = np.ones((3, 3), dtype=bool)
    cclabels, numcc = ndlabel(centerlineCandidate, strel)
    sumstrong = ndsum(strongCenterline, cclabels, list(range(1, numcc+1)))
    centerlines = np.hstack((0, sumstrong > 0)).astype('bool')
    centerlines = centerlines[cclabels]

    return centerlines