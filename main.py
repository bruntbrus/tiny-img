'''
Compress JPG and PNG images with TinyJPG (also TinyPNG).
https://tinyjpg.com/developers/reference/python

Arguments:
1. Size as name or "[width]x[height]".
2. Compression method.
3. Glob pattern for image filenames.
4. Filename extension for compressed images.
'''

import sys
from os import path
from glob import iglob
import tinify

from src.config import *
from src import utils


def main(argv) -> None:
  if not validate_api_key():
    return

  rem_cmp = get_remaining_compression_count()
  print(f'Remaining compressions: {rem_cmp} of {MAX_COMPRESS_COUNT}')

  if not rem_cmp or len(argv) == 1:
    return

  img_size = get_image_size(argv)

  if not img_size:
    return

  cmp_method = get_compress_method(argv)
  glob_pattern = get_glob_pattern(argv)
  filename_ext = get_filename_extension(argv)

  completed_count = 0
  failed_count = 0
  total_src_size = 0
  total_dst_size = 0

  print(f'Image size: {img_size[0]}x{img_size[1]}')
  print(f'Method: {cmp_method}')

  for src_path in iglob(glob_pattern):
    dst_path = path.splitext(src_path)[0] + filename_ext

    if path.exists(dst_path):
      continue

    print(f'Compress "{src_path}"...')

    if not DRY_RUN:
      if not compress_image(cmp_method, img_size, src_path, dst_path):
        failed_count += 1
        continue

      dst_size = path.getsize(dst_path)
    else:
      dst_size = 0

    completed_count += 1
    src_size = path.getsize(src_path)
    total_src_size += src_size
    total_dst_size += dst_size

    print(f'Size: {to_result(src_size, dst_size)}')

  if completed_count > 0:
    print(f'Complete: {completed_count} image(s) compressed ({failed_count} failed), {to_result(total_src_size, total_dst_size)}.')
  else:
    print(f'No image compressed ({failed_count} failed).')


def validate_api_key() -> bool:
  try:
    tinify.key = TINIFY_API_KEY
    tinify.validate()
  except tinify.Error as e:
    print(f'{e.message}')
    return False

  return True


def get_remaining_compression_count() -> int:
  return max(MAX_COMPRESS_COUNT - tinify.compression_count, 0)


def get_image_size(argv) -> tuple:
  size_name = utils.get_value(argv, 1, DEFAULT_IMAGE_SIZE_NAME).upper()
  size = None

  if size_name[0].isdigit():
    size = (int(dim) for dim in size_name.split('x', 2))
  else:
    size = IMAGE_SIZES[size_name]

  return size


def get_compress_method(argv):
  return utils.get_value(argv, 2, DEFAULT_COMPRESS_METHOD)


def get_glob_pattern(argv) -> str:
  return utils.get_value(argv, 3, DEFAULT_GLOB_PATTERN)


def get_filename_extension(argv) -> str:
  return utils.get_value(argv, 4, DEFAULT_FILENAME_EXT)


def compress_image(cmp_method, img_size, src_path, dst_path) -> bool:
  try:
    src_image = tinify.from_file(src_path)

    if img_size:
      dst_image = src_image.resize(
        method=cmp_method,
        width=img_size[0],
        height=img_size[1]
      )
    else:
      dst_image = src_image

    dst_image.to_file(dst_path)
  except tinify.Error as e:
    print(f'{e.status} {e.kind}: {e.message}')
    return False

  return True


def to_result(src_size, dst_size) -> str:
  return f'{utils.format_size(src_size)} to {utils.format_size(dst_size)} ({utils.to_percent(1 - dst_size / src_size)}%)'


if __name__ == '__main__':
  main(sys.argv)
