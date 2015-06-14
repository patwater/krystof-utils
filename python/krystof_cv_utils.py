# utility stuff related to computer vision
# uses opencv2 (cv2)

import os
import cv2
import numpy as np


def superimpose_mask_on_image(mask, image, color_delta = [20, -20, -20], slow = False):
    # superimpose mask on image, the color change being controlled by color_delta
    # TODO: currently only works on 3-channel, 8 bit images and 1-channel, 8 bit masks

    # fast, but can't handle overflows
    if not slow:
        image[:,:,0] = image[:,:,0] + color_delta[0] * (mask[:,:,0] / 255)
        image[:,:,1] = image[:,:,1] + color_delta[1] * (mask[:,:,0] / 255)
        image[:,:,2] = image[:,:,2] + color_delta[2] * (mask[:,:,0] / 255)

    # slower, but no issues with overflows
    else:
        rows, cols = image.shape[:2]
        for row in xrange(rows):
            for col in xrange(cols):
                if mask[row, col, 0] > 0:
                    image[row, col, 0] = min(255, max(0, image[row, col, 0] + color_delta[0]))
                    image[row, col, 1] = min(255, max(0, image[row, col, 1] + color_delta[1]))
                    image[row, col, 2] = min(255, max(0, image[row, col, 2] + color_delta[2]))

    return




class Image_wrapper(object):
    '''
    Wrapper around cv2's image

    Created mostly to make saving debug images easier
    '''

    def __init__(self):
        self.path         = None # path to the image file
        self.debug_prefix = None # prefix to use when saving debug images

        self.in_img = None


    def open(self, path):
        # open the image pointed to by path into self.in_img
        self.path         = path
        self.in_img       = cv2.imread(self.path)
        self.debug_prefix = os.path.join('debug', os.path.split(self.path)[1])[:-4]


    def save_debug_img(self, di, postfix):
        # save a debug image
        fn = '{}-{}.png'.format(self.debug_prefix, postfix)
        cv2.imwrite(fn, di)


    def get_blank_mask(self):
        # get a mask of all zeros of the same dimensions as self.in_img
        return np.zeros((self.in_img.shape[0], self.in_img.shape[1], 1), np.uint8)
