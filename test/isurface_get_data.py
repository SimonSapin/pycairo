#!/usr/bin/env python
"""
Test ImageSurface.get_data()
"""
import tempfile

import cairo

if not (cairo.HAS_IMAGE_SURFACE and cairo.HAS_PNG_FUNCTIONS):
  raise SystemExit ('cairo was not compiled with ImageSurface and PNG support')

width, height = 128, 128

def create_surface(cformat, w, h):
  "create black triangle on white background"
  surface = cairo.ImageSurface(cformat, w, h)
  ctx = cairo.Context(surface)

  ctx.set_source_rgb(1, 1, 1)  # white
  ctx.set_operator(cairo.OPERATOR_SOURCE)
  ctx.paint()

  # Draw out the triangle using absolute coordinates
  ctx.move_to(w/2, h/3)
  ctx.line_to(2*w/3, 2*h/3)
  ctx.rel_line_to(-1*w/3, 0)
  ctx.close_path()

  ctx.set_source_rgb(0, 0, 0)  # black
  ctx.set_line_width(15)
  ctx.stroke()
  return surface


def test_python_buffer():
  "get_data() and modify data using Python"
  surface = create_surface(cairo.FORMAT_ARGB32, width, height)
  _, f1 = tempfile.mkstemp(prefix='pycairo_', suffix='.png')
  surface.write_to_png(f1)

  buf = surface.get_data()
  stride = surface.get_stride()
  for i in range(height):
      offset = i * stride + 120
      buf[offset]     = b'\xFF'
      buf[offset + 1] = b'\x00'
      buf[offset + 2] = b'\x00'

  _, f2 = tempfile.mkstemp(prefix='pycairo_', suffix='.png')
  surface.write_to_png(f2)
  print("""\
test_python_buffer:
  original data: %s
  modified data: %s
""" % (f1, f2))


def test_numpy_and_python_buffer():
  "get_data() and modify data using numpy"
  try:
    import numpy
  except:
    print("numpy not installed")
    return

  surface = create_surface(cairo.FORMAT_ARGB32, width, height)
  _, f1 = tempfile.mkstemp(prefix='pycairo_', suffix='.png')
  surface.write_to_png(f1)

  buf = surface.get_data()

  a = numpy.ndarray(shape=(w,h,4), dtype=numpy.uint8, buffer=buf)

  # draw a vertical line
  a[:,40,0] = 255  # byte 0 is blue on little-endian systems
  a[:,40,1] = 0
  a[:,40,2] = 0

  _, f2 = tempfile.mkstemp(prefix='pycairo_', suffix='.png')
  surface.write_to_png(f2)
  print("""\
test_numpy_and_python_buffer:
  original data: %s
  modified data: %s
""" % (f1, f2))


test_python_buffer()
test_numpy_and_python_buffer()
