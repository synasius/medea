import web, os
import logging

DEBUG = False

# Setup logging
def setup_logger():
    """ Configure logger """
    logger = logging.getLogger("medea")
    formatter = logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    shandler = logging.StreamHandler()
    shandler.setLevel(DEBUG and logging.DEBUG or logging.WARNING)
    shandler.setFormatter(formatter)

    fhandler = logging.FileHandler("medea.log")
    fhandler.setLevel(DEBUG and logging.DEBUG or logging.WARNING)
    fhandler.setFormatter(formatter)

    logger.addHandler(shandler)
    logger.addHandler(fhandler)
    logger.setLevel(logging.DEBUG)

    return logger

LOG = setup_logger()

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(BASE_PATH, 'templates/')
STATIC_FILES = "static/"
X3D_PATH = os.path.join(STATIC_FILES, 'x3d')
IMAGES_PATH = os.path.join(STATIC_FILES, 'images')

# object library settings
LIBRARY_PATH = os.path.join(X3D_PATH, 'library')
LIBRARY_NO_THUMB = os.path.join(IMAGES_PATH, 'nothumb.png')

# Database settings

# Web.py caching
cache = False

