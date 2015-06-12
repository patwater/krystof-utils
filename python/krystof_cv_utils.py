# utility stuff related to computer vision
# uses opencv2 (cv2)

import os
import cv2



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
