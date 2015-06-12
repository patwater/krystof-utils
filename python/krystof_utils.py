# General Python utility functions

import inspect



def MSG(body):
    # print a message, preceded by the calling function's file and line number
    try:
        stack = inspect.stack()
        frame = stack[1]

        # filename: only show the last part
        fn = frame[1]
        slash = fn.rfind('/')
        if slash != -1:
            fn = fn[slash + 1 :]

        print("{}:{} {}".format(fn, frame[2], body))

    except Exception as e:
        print("Exception encountered in MSG(): {}".format(e))
        print(body)



def TODO(body = ''):
    # print a really big 'TODO' message
    try:
        stack = inspect.stack()
        frame = stack[1]

        # filename: only show the last part
        fn = frame[1]
        slash = fn.rfind('/')
        if slash != -1:
            fn = fn[slash + 1 :]

        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!! TODO: {}:{}:{}(): {}\n".\
              format(fn, frame[2], frame[3], body))

    except Exception as e:
        print("Exception encountered in TODO(): {}".format(e))
        print(body)
