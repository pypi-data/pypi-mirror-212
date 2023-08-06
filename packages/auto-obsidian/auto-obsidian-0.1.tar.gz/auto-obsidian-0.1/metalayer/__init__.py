import os

METALAYER_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(METALAYER_PATH, 'data/')

ACTIVITY_LOG_DIR = os.path.join(DATA_DIR, 'activity_log/')
CAPTURE_DIR = os.path.join(DATA_DIR, 'captures/')
ICON_DIR = os.path.join(DATA_DIR, 'icons/')
THUMBNAIL_DIR = os.path.join(DATA_DIR, 'thumbnails/')

import os
if os.getcwd().endswith('metalayer'):
    for dir_name in [ACTIVITY_LOG_DIR, CAPTURE_DIR, ICON_DIR, THUMBNAIL_DIR]:
        os.makedirs(dir_name, exist_ok=True)
