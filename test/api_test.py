'''test pycairo API
- can be expanded later as required.
- is not able to test the quality of images created. We assume cairo itself
  tests for this.
'''
import io
import zlib
import base64
import tempfile as tfi

import cairo
import py.test as test


def test_context():
  if cairo.HAS_IMAGE_SURFACE:
    f, w, h = cairo.FORMAT_ARGB32, 100, 100
    s = cairo.ImageSurface(f, w, h)
    ctx = cairo.Context(s)
    ctx.set_source_rgb(1.0, 1.0, 1.0)
    ctx.set_operator(cairo.OPERATOR_SOURCE)
    ctx.paint()


def test_matrix():
  m = cairo.Matrix()
  m.rotate(10)
  m.scale(1.5, 2.5)
  m.translate(10, 20)


def test_path():
  # AttributeError: 'module' object has no attribute 'Path'
  test.raises(AttributeError, "p = cairo.Path()")
  # see examples/warpedtext.py


def test_pattern():
  # TypeError: The Pattern type cannot be instantiated
  test.raises(TypeError, "p = cairo.Pattern()")

  r,g,b,a = 0.1, 0.2, 0.3, 0.4
  p = cairo.SolidPattern(r,g,b,a)
  assert p.get_rgba() == (r,g,b,a)

  # SurfacePattern

  # TypeError: The Gradient type cannot be instantiated
  test.raises(TypeError, "p = cairo.Gradient()")

  x0,y0,x1,y1 = 0.0, 0.0, 0.0, 1.0
  p = cairo.LinearGradient(x0,y0,x1,y1)
  assert p.get_linear_points() == (x0,y0,x1,y1)
  p.add_color_stop_rgba(1, 0, 0, 0, 1)
  p.add_color_stop_rgba(0, 1, 1, 1, 1)

  cx0, cy0, radius0, cx1, cy1, radius1 = 1.0, 1.0, 1.0, 2.0, 2.0, 1.0
  p = cairo.RadialGradient(cx0, cy0, radius0, cx1, cy1, radius1)
  assert p.get_radial_circles() == (cx0, cy0, radius0, cx1, cy1, radius1)
  p.add_color_stop_rgba(0, 1, 1, 1, 1)
  p.add_color_stop_rgba(1, 0, 0, 0, 1)


def test_surface():
  # TypeError: The Surface type cannot be instantiated
  test.raises(TypeError, "s = cairo.Surface()")

  if cairo.HAS_IMAGE_SURFACE:
    f, w, h = cairo.FORMAT_ARGB32, 100, 100
    s = cairo.ImageSurface(f, w, h)
    assert s.get_format() == f
    assert s.get_width() == w
    assert s.get_height() == h

  if cairo.HAS_PDF_SURFACE:
    f, w, h = tfi.TemporaryFile(mode='w+b'), 100, 100
    s = cairo.PDFSurface(f, w, h)

  if cairo.HAS_PS_SURFACE:
    f, w, h = tfi.TemporaryFile(mode='w+b'), 100, 100
    s = cairo.PSSurface(f, w, h)

  if cairo.HAS_RECORDING_SURFACE:
    s = cairo.RecordingSurface(cairo.CONTENT_COLOR, None)
    s = cairo.RecordingSurface(cairo.CONTENT_COLOR, (1,1,10,10))

  if cairo.HAS_SVG_SURFACE:
    f, w, h = tfi.TemporaryFile(mode='w+b'), 100, 100
    s = cairo.SVGSurface(f, w, h)


def test_text():
  pass


def test_region():
  a = cairo.Region()
  assert a.is_empty() == True
  assert a.num_rectangles() == 0

  b = cairo.RectangleInt(1, 2, 10, 12)
  d = cairo.RectangleInt(1, 1, 10, 12)
  e = cairo.RectangleInt(1, 3, 8, 12)
  assert (b.x, b.y, b.width, b.height) == (1, 2, 10, 12)
  c = cairo.Region((b, e))
  assert not c.is_empty()
  assert c.num_rectangles() == 2
  assert c.get_rectangle(1).y == 14

  ex = c.get_extents()
  assert ex == cairo.RectangleInt(1, 2, 10, 13)
  assert c.contains_rectangle(d) == cairo.REGION_OVERLAP_PART

  c.translate(10, 20)
  assert c.contains_rectangle(d) == cairo.REGION_OVERLAP_OUT
  assert c.get_rectangle(1) == cairo.RectangleInt(11, 34, 8, 1)

  cp = c.copy()
  assert c.num_rectangles() == cp.num_rectangles()
  assert c.get_rectangle(0) == cp.get_rectangle(0)
  assert c == cp
  assert 3 != c
  assert c != "test"

  c = cairo.Region((b, e))
  c.intersect(d)
  assert c.num_rectangles() == 1
  assert c.get_rectangle(0) == cairo.RectangleInt(1, 2, 10, 11)

  c = cairo.Region((b, e))
  c.subtract(d)
  assert c.num_rectangles() == 2
  assert c == cairo.Region([
      cairo.RectangleInt(1, 13, 10, 1), cairo.RectangleInt(1, 14, 8, 1) ])

  d = cairo.Region(d)
  c = cairo.Region((b, e))
  c.subtract(d)
  assert c.num_rectangles() == 2
  assert c.get_rectangle(0) == cairo.RectangleInt(1, 13, 10, 1)

  c = cairo.Region((b, e))
  c.union(d)
  assert c.num_rectangles() == 2
  assert c == cairo.Region([
      cairo.RectangleInt(1, 1, 10, 13), cairo.RectangleInt(1, 14, 8, 1) ])

  c = cairo.Region((b, e))
  c.xor(d)
  assert c.num_rectangles() == 3
  assert c == cairo.Region([
      cairo.RectangleInt(1, 1, 10, 1),
      cairo.RectangleInt(1, 14, 8, 1),
      cairo.RectangleInt(1, 13, 10, 1),
      ])


def test_mime_data():
    # A 1x1 pixel white image:
    png_bytes = base64.b64decode(
        b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAAAAAA6fptVAAAACklEQV'
        b'QI12P4DwABAQEAG7buVgAAAABJRU5ErkJggg==')
    jpeg_bytes = zlib.decompress(base64.b64decode(
        b'eJz7f+P/AwYBLzdPNwZGRkYGDyBk+H+bwRnEowj8P8TAzcHACDJHkOH/EQYRIBsV'
        b'cP6/xcDBCBJlrLcHqRBAV8EAVcHIylSPVwGbPQEFjPaK9XDrBAipBSq4CQB9jiS0'))

    def render(image, surface_type):
        file_like = io.BytesIO()
        surface = surface_type(file_like, 100, 100)
        context = cairo.Context(surface)
        context.set_source_surface(image, 0, 0)
        context.paint()
        surface.finish()
        pdf_bytes = file_like.getvalue()
        return pdf_bytes

    image = cairo.ImageSurface.create_from_png(io.BytesIO(png_bytes))
    assert image.get_mime_data('image/jpeg') is None

    pdf_bytes = render(image, cairo.PDFSurface)
    assert pdf_bytes.startswith(b'%PDF')
    assert b'/Filter /DCTDecode' not in pdf_bytes

    image.set_mime_data('image/jpeg', jpeg_bytes)
    jpeg_bytes = jpeg_bytes[:]  # Copy, drop a reference to the old object.
    assert image.get_mime_data('image/jpeg')[:] == jpeg_bytes

    pdf_bytes = render(image, cairo.PDFSurface)
    assert pdf_bytes.startswith(b'%PDF')
    # JPEG-encoded image:
    assert b'/Filter /DCTDecode' in pdf_bytes

    image.set_mime_data('image/jpeg', None)
    assert image.get_mime_data('image/jpeg') is None
