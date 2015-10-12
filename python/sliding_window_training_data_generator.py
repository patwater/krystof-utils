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

        # files where to keep track of what's been processed, and how
        self.POSFILE        = 'positives.json'
        self.NEGFILE        = 'negatives.json'
        self.NEUTRAL_FILE   = 'neutral.json'
        self.PROCESSED_FILE = 'processed.txt'


    def train(self):
        '''
        TODO
        '''

        # get the list of images we've alredy processed
        if not os.path.isfile(self.PROCESSED_FILE):
            # make the file if it didn't exist
            with open(self.PROCESSED_FILE, 'a') as fp:
                pass
        with open(self.PROCESSED_FILE, 'r') as fp:
            processed = [s.strip() for s in fp.readlines()]

        # for each file in the source directory
        for fn in os.listdir(self.SOURCEDIR):
        
            # is it an image?
            if fn[-4:] != '.jpg':
                continue

            # have we processed this image already?
            # if so, skip it
            if fn in processed:
                MSG('skipping {} (already processed)'.format(fn))
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

                # get some valid input from the user
                key = None
                while key not in [27, 65363, 65361, 65364]:

                    key = cv2.waitKey(0)

                    # escape: kill the program
                    if key == 27:
                        MSG('Exiting.')
                        return

                    # right arrow: 65363 -> positive region
                    elif key == 65363:
                        MSG('POSITIVE')

                    # left  arrow: 65361 -> negative region
                    elif key == 65361:
                        MSG('negative')

                    # down  arrow: 65364 -> neutral / unknown / N/A / skip
                    elif key == 65364:
                        MSG('neutral')

                    # not valid input: ask again
                    else:
                        MSG('Valid input values:\n'
                            'right arrow: positive region\n'
                            'left  arrow: negative region\n'
                            'down  arrow: not sure\n'
                            'escape     : exit the program')

                # get the next region
                region = sw.get_next()

            # mark this image as processed
            with open(self.PROCESSED_FILE, 'a') as fp:
                fp.write('{}\n'.format(fn))



if __name__ == '__main__':

    # TODO: parse user input

    # TODO: keep track of which images were already processed
    
    gen = Training_data_generator()
    gen.train()
