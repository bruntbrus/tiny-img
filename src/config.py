'''
Configuration.
'''

# Main settings
TINIFY_API_KEY = 'GXqT3rXwqFzDQqp26L0PPzClbY0FScBD'
MAX_COMPRESS_COUNT = 500
DEFAULT_IMAGE_SIZE_NAME = 'SAME'
DEFAULT_COMPRESS_METHOD = 'cover' # scale | fit | cover | thumb
DEFAULT_FILE_TYPE = 'jpg'
DEFAULT_GLOB_PATTERN = '*.' + DEFAULT_FILE_TYPE
DEFAULT_FILENAME_EXT = ' - compressed.' + DEFAULT_FILE_TYPE

# Image sizes
IMAGE_SIZES = {
  'SAME': None,
  'QVGA': (320, 240),
  'VGA': (640, 480),
  'SVGA': (800, 600),
  'HD': (1280, 720),
  'FHD': (1920, 1080),
  'UHD': (3840, 2160),
  'A4': (2480, 3508), # 300 PPI, 210 x 297 mm (8.27 x 11.69 inch)
}

# No side effects
DRY_RUN = False
