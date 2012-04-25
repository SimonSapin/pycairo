#!/usr/bin/env python
"""test cairo.ImageSurface.create_for_data()
"""

import array
import tempfile

import cairo

if not (cairo.HAS_IMAGE_SURFACE and cairo.HAS_PNG_FUNCTIONS):
  raise SystemExit ('cairo was not compiled with ImageSurface and PNG support')


def test_python_array():
  h, fileName = tempfile.mkstemp(prefix='pycairo_', suffix='.png')
  width, height = 255, 255
  data = array.array('B', [0] * width * height * 4)

  for y in range(height):
    for x in range(width):
      offset = (x + (y * width)) * 4
      alpha = y

      # cairo.FORMAT_ARGB32 uses pre-multiplied alpha
      data[offset+0] = int(x * alpha/255.0) # B
      data[offset+1] = int(y * alpha/255.0) # G
      data[offset+2] = 0                    # R
      data[offset+3] = alpha                # A

  surface = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32,
                                               width, height)
  ctx = cairo.Context(surface)
  surface.write_to_png(fileName)
  print("see %s output file" % fileName)


def test_numpy_array():
  "create_for_data() using numpy"
  try:
    import numpy
  except:
    print("numpy not installed")
    return

  h, fileName = tempfile.mkstemp(prefix='pycairo_', suffix='.png')
  width, height = 255, 255
  data = numpy.ndarray (shape=(height,width,4), dtype=numpy.uint8)

  for x in range(width):
    for y in range(height):
      alpha = y

      # cairo.FORMAT_ARGB32 uses pre-multiplied alpha
      data[y][x][0] = int(x * alpha/255.0) # B
      data[y][x][1] = int(y * alpha/255.0) # G
      data[y][x][2] = 0                    # R
      data[y][x][3] = alpha                # A

  surface = cairo.ImageSurface.create_for_data (data, cairo.FORMAT_ARGB32,
                                                width, height)
  ctx = cairo.Context(surface)
  surface.write_to_png(fileName)
  print("see %s output file" % fileName)


test_python_array()
test_numpy_array()
