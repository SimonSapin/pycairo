'''test for reference counting problems.

If a Python object is garbage collected while another object is using its
data, you will get a segmentation fault.
'''

import array
import gc
import tempfile as tfi

import cairo
import py.test as test

width, height = 256, 256

def draw(ctx, width, height):
  "example draw code"
  ctx.scale(width/1.0, height/1.0)

  pat = cairo.LinearGradient(0.0, 0.0, 0.0, 1.0)
  pat.add_color_stop_rgba(1, 0, 0, 0, 1)
  pat.add_color_stop_rgba(0, 1, 1, 1, 1)
  ctx.rectangle(0,0,1,1)
  ctx.set_source(pat)
  ctx.fill()


def test_create_for_stream():
  def run_test(surface_method, suffix):
    _, fo = tfi.mkstemp(prefix='pycairo_', suffix=suffix)
    surface = surface_method(fo, width, height)
    ctx = cairo.Context(surface)

    del fo  # test that 'fo' is referenced to keep it alive
    gc.collect()

    draw(ctx, width, height)
    ctx.show_page()
    surface.finish()

  if cairo.HAS_PDF_SURFACE:
    run_test(cairo.PDFSurface, '.pdf')
  if cairo.HAS_PS_SURFACE:
    run_test(cairo.PSSurface, '.ps')
  if cairo.HAS_SVG_SURFACE:
    run_test(cairo.SVGSurface, '.svg')


def test_get_data():
  surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)

  memView = surface.get_data()

  del surface  # test that 'surface' is referenced to keep it alive
  gc.collect()

  memView[0] = b'\xFF'
  data = memView.tobytes()


def test_create_for_data():
  data = array.array('B', [0] * width * height * 4)

  surface = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32,
                                               width, height)
  ctx = cairo.Context(surface)

  del data  # test that 'data' is referenced to keep it alive
  gc.collect()

  draw(ctx, width, height)

  _, fo = tfi.mkstemp(prefix='pycairo_', suffix='.png')
  surface.write_to_png(fo)
