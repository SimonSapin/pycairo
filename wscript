# -*- python -*-

import os

top = '.'
out = 'build_directory'
d = top

APPNAME='pycairo'
VERSION='1.8.11'
cairo_version_required = '1.8.10'


def set_options(ctx):
  print('  %s/set_options()' %d)
  ctx.tool_options('compiler_cc')
  ctx.tool_options('python') # options for disabling pyc or pyo compilation


def init():  # run at start of any waf invocation
  print('  %s/init()' %d)

def shutdown():  # run at end of any waf invocation
  print('  %s/shutdown()' %d)


def configure(ctx):
  print('  %s/configure()' %d)

  env = ctx.env
  ctx.check_tool('misc')
  ctx.check_tool('compiler_cc')
  ctx.check_tool('python')
  ctx.check_python_version((3,1,0))
  ctx.check_python_headers()
  ctx.check_cfg(package='cairo', atleast_version=cairo_version_required,
                args='--cflags --libs')

  # add gcc options
  if env['CC_NAME'] == 'gcc':
    env.append_unique('CCFLAGS', ['-std=c99', '-Wall'])

  version = [int(s) for s in VERSION.split('.')]
  ctx.define('VERSION', VERSION)
  ctx.define('PYCAIRO_VERSION_MAJOR', version[0])
  ctx.define('PYCAIRO_VERSION_MINOR', version[1])
  ctx.define('PYCAIRO_VERSION_MICRO', version[2])

  ctx.write_config_header('src/config.h')

  import Options
  print("%-40s : %s" % ('Prefix', Options.options.prefix))


def build(ctx):
  print('  %s/build()' %d)
  ctx.add_subdirs('src')

  # generate and install the .pc file
  obj = ctx.new_task_gen('subst')
  obj.source = 'py3cairo.pc.in'
  obj.target = 'py3cairo.pc'
  obj.dict = {
    'VERSION'   : VERSION,
    'prefix'    : ctx.env['PREFIX'],
    'includedir': os.path.join(ctx.env['PREFIX'], 'include'),
    }
  obj.install_path = os.path.join(ctx.env['PREFIX'], 'lib', 'pkgconfig')


#def dist():  # create archives of project
#  print('  %s/dist()' %d)
# dist is predefined


def dist_hook():
  # remove unwanted files from the archive

  # individual files
  for f in [
    'RELEASING',
    'examples/cairo_snippets/c_to_python.py',
    'doc/html_docs_create.sh',
    'doc/html_docs_upload.sh',
    ]:
    os.remove(f)

  # rm examples/*.{pdf,png,ps,svg}
  D='examples'
  for f in os.listdir(D):
    if f.endswith(('.pdf', '.png', '.ps', '.svg')):
      os.remove(os.path.join(D, f))

  D='examples/cairo_snippets/snippets'
  for f in os.listdir(D):
    if f.endswith(('.pdf', '.png', '.ps', '.svg')):
      os.remove(os.path.join(D, f))
