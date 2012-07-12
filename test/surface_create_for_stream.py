#!/usr/bin/env python
"""
Test PDF/PS/SVG constructors (using streams)
"""

import gc
import math
import sys
#import io.Bytes

import cairo


class C(object):
  """a file-like object (for testing), it simulates sys.stdout
  """
  def __init__ (self):
    self.closed = False

  def write(self, s):
    """just echo to stdout, without newlines"""
    if self.closed:
      raise ValueError ("I/O operation on closed file")
    sys.stdout.write(s)

  def close(self):
    self.closed = True


WIDTH, HEIGHT  = 256, 256

# a selection of possible args to surface.write_to_png()
fo = sys.stdout  # only compatible with str/text objects - SVG
#fo = C()

#fo = '/tmp/f.pdf'
#fo = open('/tmp/f.pdf', 'wb')
#surface = cairo.PDFSurface(fo, WIDTH, HEIGHT)

#fo = '/tmp/f.ps'
#fo = open('/tmp/f.ps', 'wb')
#surface = cairo.PSSurface(fo, WIDTH, HEIGHT)

#fo = '/tmp/f.svg'
#fo = open('/tmp/f.svg', 'wt')
surface = cairo.SVGSurface(fo, WIDTH, HEIGHT)

#fo.close()  # this should cause: ValueError: I/O operation on closed file


#sys.stdout.write ('1\n'); sys.stdout.flush()
ctx = cairo.Context(surface)

#del fo  # test that 'fo' is referenced to keep it alive
#gc.collect()

#fo.close()  # this should cause: ValueError: I/O operation on closed file

ctx.scale(WIDTH/1.0, HEIGHT/1.0)

pat = cairo.LinearGradient(0.0, 0.0, 0.0, 1.0)
pat.add_color_stop_rgba(1, 0, 0, 0, 1)
pat.add_color_stop_rgba(0, 1, 1, 1, 1)

ctx.rectangle(0,0,1,1)
ctx.set_source(pat)
ctx.fill()

pat = cairo.RadialGradient(0.45, 0.4, 0.1,
                            0.4,  0.4, 0.5)
pat.add_color_stop_rgba(0, 1, 1, 1, 1)
pat.add_color_stop_rgba(1, 0, 0, 0, 1)

ctx.set_source(pat)
ctx.arc(0.5, 0.5, 0.3, 0, 2 * math.pi)
ctx.fill()

ctx.show_page()
surface.finish()

# for testing io.Bytes: get data and write to file
#string = fo.getvalue()
#f2 = file('/tmp/f.ps', 'wb')
#f2.write(string)
#f2.close()
