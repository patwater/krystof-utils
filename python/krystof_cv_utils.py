# utility stuff related to computer vision
# uses opencv (cv2)

import os
import cv2
import numpy as np

from krystof_utils import MSG, TODO


def superimpose_mask_on_image(mask, image, color_delta = [20, -20, -20]):
    # superimpose mask on image, the color change being controlled by color_delta
    # TODO: currently only works on 3-channel, 8 bit images and 1-channel, 8 bit masks

    image = image.astype(np.int16)

    image[:, :, 0] = np.clip(image[:, :, 0] + color_delta[0] * (mask[:, :, 0] / 255), 0, 255)
    image[:, :, 1] = np.clip(image[:, :, 1] + color_delta[1] * (mask[:, :, 0] / 255), 0, 255)
    image[:, :, 2] = np.clip(image[:, :, 2] + color_delta[2] * (mask[:, :, 0] / 255), 0, 255)

    image = image.astype(np.uint8)
    return image



def get_std_dev_image(image, side = 5):
    # get the standard deviation for each pixel w.r.t. a side x side window

    # work with floats
    imgf = image.astype(np.float32)

    # get the mean
    mean = cv2.blur(imgf, (side, side))

    # get the mean of the squared image
    mean_sq = cv2.blur(cv2.multiply(imgf, imgf), (side, side))

    # std deviation = sqrt( expectation(x^2) - (expecation(x)^2) )
    std = cv2.sqrt(mean_sq - cv2.multiply(mean, mean))

    return std



class Image_wrapper(object):
    '''
    Wrapper around cv2's image

    Created mostly to make saving debug images easier
    '''

    def __init__(self):
        self.path            = None # path to the image file
        self.debug_prefix    = None # prefix to use when saving debug images
        self.filename_no_ext = None # filename, no path, no extension (e.g. "my-image")

        self.in_img = None # input image (color)
        self.in_gs  = None # input image (grayscale)


    def open(self, path):
        # open the image pointed to by path into self.in_img
        self.path            = path
        self.filename_no_ext = os.path.split(self.path)[1][:-4]
        self.in_img          = cv2.imread(self.path)
        self.debug_prefix    = os.path.join('debug', self.filename_no_ext)

        # get a grayscale version of the image
        if self.in_img.shape[2] > 1:
            self.in_gs = cv2.cvtColor(self.in_img, cv2.COLOR_BGR2GRAY)
        else:
            self.in_gs = self.in_img.copy()


    def save_debug_img(self, di, postfix):
        # save a debug image
        fn = '{}-{}.png'.format(self.debug_prefix, postfix)
        cv2.imwrite(fn, di)


    def get_blank_mask(self):
        # get a mask of all zeros of the same dimensions as self.in_img
        return np.zeros((self.in_img.shape[0], self.in_img.shape[1], 1), np.uint8)



class Sliding_window(object):
    # Given an input image, generates regions on it
    # Multi-scale sliding window

    # TODO: allow user to set params
    def __init__(self):
        self.WINDOW_SIZE = 256 #128 # pixels
        self.STEP        = 128 # 32 # pixels
        self.MAXSCALE    =   2 # image gets shrunk at most 1/this

        self.img   = None
        self.scale = 1
        self.xmin  = 0
        self.xmax  = self.WINDOW_SIZE
        self.ymin  = 0
        self.ymax  = self.WINDOW_SIZE
        self.rows  = 0
        self.cols  = 0


    def load(self, img):
        self.img  = img
        self.rows, self.cols = self.img.shape[:2]
    
        # reset state
        self.scale = 1
        self.xmin  = -self.STEP
        self.xmax  = self.WINDOW_SIZE - self.STEP
        self.ymin  = 0
        self.ymax  = self.WINDOW_SIZE


        
    def get_next(self):
        # get the next region
        # returns the [xmin, xmax, ymin, ymax]

        if self.img is None:
            raise Exception('No image loaded')

        # col
        self.xmin += self.STEP
        self.xmax += self.STEP

        # next row?
        if self.xmax * self.scale > self.cols:
            self.xmin  = 0
            self.xmax  = self.WINDOW_SIZE
            self.ymin += self.STEP
            self.ymax += self.STEP            

        #MSG('[{}, {}], [{}, {}]; image is {} x {}'.
        #    format(self.xmin, self.ymin, self.xmax, self.ymax,
        #           self.cols, self.rows))

        # next scale?
        if self.ymax * self.scale > self.rows:

            self.scale *= 2

            # are we done?
            if self.scale > self.MAXSCALE:
                return None

            self.xmin  = 0
            self.xmax  = self.WINDOW_SIZE
            self.ymin  = 0
            self.ymax  = self.WINDOW_SIZE

        # return the current region
        return [x * self.scale for x in [self.xmin, self.xmax, self.ymin, self.ymax]]

