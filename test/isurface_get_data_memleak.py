#!/usr/bin/env python
"""test cairo.ImageSurface.get_data() for a memory leak
"""

import array
import resource
import tempfile

import cairo


pagesize = resource.getpagesize()

if not (cairo.HAS_IMAGE_SURFACE and cairo.HAS_PNG_FUNCTIONS):
  raise SystemExit ('cairo was not compiled with ImageSurface and PNG support')

width, height = 32, 32

while True:
  for i in range(100000):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)
    data = surface.get_data()
    b = memoryview(memoryview(data))
    del surface
    del ctx
    b = bytes(data)

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    #ctx = cairo.Context(surface)
    b = bytes(surface.get_data())

  print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * pagesize)
