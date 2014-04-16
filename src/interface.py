#!/usr/bin/env python3
'''
blueshift-curse – Blueshift extension with IPC and an ncurses front-end
Copyright © 2014  Mattias Andrée (maandree@member.fsf.org)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import sys



PROGRAM_NAME = 'blueshift-curse'
'''
:str  The name of the program
'''

PROGRAM_VERSION = '1.0'
'''
:str  The version of the program
'''



## Set process title
def setproctitle(title):
    '''
    Set process title
    
    @param  title:str  The title of the process
    '''
    import ctypes
    try:
        # Remove path, keep only the file,
        # otherwise we get really bad effects, namely
        # the name title is truncates by the number
        # of slashes in the title. At least that is
        # the observed behaviour when using procps-ng.
        title = title.split('/')[-1]
        # Create strng buffer with title
        title = title.encode(sys.getdefaultencoding(), 'replace')
        title = ctypes.create_string_buffer(title)
        if 'linux' in sys.platform:
            # Set process title on Linux
            libc = ctypes.cdll.LoadLibrary('libc.so.6')
            libc.prctl(15, ctypes.byref(title), 0, 0, 0)
        elif 'bsd' in sys.platform:
            # Set process title on at least FreeBSD
            libc = ctypes.cdll.LoadLibrary('libc.so.7')
            libc.setproctitle(ctypes.create_string_buffer(b'-%s'), title)
    except:
        pass
setproctitle(sys.argv[0])


## Load extension and configurations via blueshiftrc
# No configuration script has been selected explicitly,
# so select one automatically.
g, l = globals(), dict(locals())
for key in l:
    g[key] = l[key]
if config_file is None:
    # Possible auto-selected configuration scripts,
    # earlier ones have precedence, we can only select one.
    files = []
    def add_files(var, *ps, multi = False):
        if var == '~':
            try:
                # Get the home (also known as initial) directory of the real user
                import pwd
                var = pwd.getpwuid(os.getuid()).pw_dir
            except:
                return
        else:
            # Resolve environment variable or use empty string if none is selected
            if (var is None) or (var in os.environ) and (not os.environ[var] == ''):
                var = '' if var is None else os.environ[var]
            else:
                return
        paths = [var]
        # Split environment variable value if it is a multi valeu variable
        if multi and os.pathsep in var:
            paths = [v for v in var.split(os.pathsep) if not v == '']
        # Add files according to patterns
        for p in ps:
            p = p.replace('/', os.sep).replace('%', PROGRAM_NAME)
            for v in paths:
                files.append(v + p)
    add_files('XDG_CONFIG_HOME', '/%/%rc', '/%rc')
    add_files('HOME',            '/.config/%/%rc', '/.%rc')
    add_files('~',               '/.config/%/%rc', '/.%rc')
    add_files('XDG_CONFIG_DIRS', '/%rc', multi = True)
    add_files(None,              '/etc/%rc')
    for file in files:
        # If the file we exists,
        if os.path.exists(file):
            # select it,
            config_file = file
            # and stop trying files with lower precedence.
            break
# As the zeroth argument for the configuration script,
# add the configurion script file. Just like the zeroth
# command line argument is the invoked command.
conf_opts = [config_file] + conf_opts
if config_file is not None:
    code = None
    # Read configuration script file
    with open(config_file, 'rb') as script:
        code = script.read()
    # Decode configurion script file and add a line break
    # at the end to ensure that the last line is empty.
    # If it is not, we will get errors.
    code = code.decode('utf-8', 'error') + '\n'
    # Compile the configuration script,
    code = compile(code, config_file, 'exec')
    # and run it, with it have the same
    # globals as this module, so that it can
    # not only use want we have defined, but
    # also redefine it for us.
    exec(code, g)

