#!/usr/bin/python
'''
Utility to generate training regions on input images
User tells the software whether each region is positive or negative

Written/tested with Python 2.7.6 and OpenCV 3.0.0
'''

import os

import cv2

from krystof_utils import MSG, TODO
import krystof_cv_utils


class Training_data_generator(object):
    '''

    '''

    def __init__(self):
        # path to the directories where to save positive and negative training regions
        # TODO: let user set these
        self.POSDIR = 'positive'
        self.NEGDIR = 'negative'
        
        # directory from where to read the images
        self.SOURCEDIR = 'raw_images'


    def train(self):
        '''
        TODO
        '''

        # for each file in the source directory
        for fn in os.listdir(self.SOURCEDIR):
        
            # is it an image?
            if fn[-4:] != '.jpg':
                continue

            fullfn = os.path.join(self.SOURCEDIR, fn)
            MSG("Opening {}".format(fullfn))

            img = krystof_cv_utils.Image_wrapper()
            img.open(fullfn)

            # testing
            img.save_debug_img(img.in_img, 'input')

            sw = krystof_cv_utils.Sliding_window()
            sw.load(img.in_img)
            region = sw.get_next()

            cv2.namedWindow('img')

            while region is not None:
                #MSG('region: {}'.format(region))

                # create an image to show the current region to the user
                di = img.in_img.copy()

                # draw the region on the debug image
                cv2.rectangle(di, (region[0], region[2]), (region[1], region[3]),
                              (0, 255, 0), # green
                              3) # thickness

                # show the image
                cv2.imshow('img', di)

                # TODO: get user input (good/bad/unsure)
                cv2.waitKey(0)

                region = sw.get_next()

                



if __name__ == '__main__':

    # TODO: parse user input

    # TODO: keep track of which images were already processed
    
    gen = Training_data_generator()
    gen.train()
