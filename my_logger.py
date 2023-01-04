# save logs
import logging


# set up logging to file 
# print both to the console and to a file
logging.basicConfig(level=logging.INFO,
                    # write filename and line number
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s %(filename)s:%(lineno)d',
                    datefmt='%m-%d %H:%M',
                    filename='plate_detection.log',
                    filemode='a',
                    )

# # define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# # set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s %(filename)s:%(lineno)d')
# # tell the handler to use this format
console.setFormatter(formatter)

# # add the handler to the root logger
logging.getLogger('').addHandler(console)

logger = logging.getLogger(__name__)