'''
Utilities.
'''

def get_value(items, i, def_val=None):
  return items[i] if len(items) > i else def_val


def format_size(num) -> str:
  if num < 1024:
    unit = 'B'
  elif num < 1024 ** 2:
    num = round(num / 1024, 2)
    unit = 'KB'
  else:
    num = round(num / 1024 ** 2, 2)
    unit = 'MB'

  return str(num) + unit


def to_percent(num) -> float:
  return round(num * 100, 2)
