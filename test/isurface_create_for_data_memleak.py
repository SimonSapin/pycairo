#!/usr/bin/env python
"""test cairo.ImageSurface.create_for_data() for memory leaks
"""

import array
import resource

import cairo


pagesize = resource.getpagesize()

if not (cairo.HAS_IMAGE_SURFACE and cairo.HAS_PNG_FUNCTIONS):
  raise SystemExit ('cairo was not compiled with ImageSurface and PNG support')

width, height = 255, 255
lst = [0] * width * height * 4

c = 1
while True:
  for i in range(50):
    data = array.array('B', lst)
    surface = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32,
                                                 width, height)
    ctx = cairo.Context(surface)

  print(c, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * pagesize)
  c += 1
