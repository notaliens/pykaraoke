#!/usr/bin/env python
#******************************************************************************
#****                                                                      ****
#**** Copyright (C) 2010  Kelvin Lawson (kelvinl@users.sourceforge.net)    ****
#**** Copyright (C) 2010  PyKaraoke Development Team                       ****
#****                                                                      ****
#**** This library is free software; you can redistribute it and/or        ****
#**** modify it under the terms of the GNU Lesser General Public           ****
#**** License as published by the Free Software Foundation; either         ****
#**** version 2.1 of the License, or (at your option) any later version.   ****
#****                                                                      ****
#**** This library is distributed in the hope that it will be useful,      ****
#**** but WITHOUT ANY WARRANTY; without even the implied warranty of       ****
#**** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU    ****
#**** Lesser General Public License for more details.                      ****
#****                                                                      ****
#**** You should have received a copy of the GNU Lesser General Public     ****
#**** License along with this library; if not, write to the                ****
#**** Free Software Foundation, Inc.                                       ****
#**** 59 Temple Place, Suite 330                                           ****
#**** Boston, MA  02111-1307  USA                                          ****
#******************************************************************************

import glob
import os
import os.path

from distutils.errors import CCompilerError
from distutils.errors import DistutilsExecError
from distutils.errors import DistutilsPlatformError

from setuptools import setup
from setuptools import find_packages
from setuptools.command.build_ext import build_ext
from setuptools import Extension

windows = os.name == 'nt'

# optional code optimizations
cdgaux_ext_c = os.path.join('pykaraoke', '_pycdgAux.c')
cdgaux_ext = Extension(
    "pykaraoke._pycdgAux",
    [os.path.normcase(cdgaux_ext_c)],
    libraries = ['SDL'],
    )
    
# These data files only make sense on Unix-like systems.
if not windows:
    data_files = [
        ('share/applications', ['pykaraoke/install/pykaraoke.desktop',
                                'pykaraoke/install/pykaraoke_mini.desktop']),
        ('share/pykaraoke/icons', ['pykaraoke/icons/pykaraoke.xpm',]),
        ]

# These are the basic keyword arguments we will pass to distutil's
# setup() function.
cmdclass = {}
setupArgs = {
  'name' : "pykaraoke",
  'version' : '0.7.6dev',
  'description' : 'PyKaraoke = CD+G/MPEG/KAR Karaoke Player',
  'maintainer' : 'Kelvin Lawson',
  'maintainer_email' : 'kelvin@kibosh.org',
  'url' : 'http://www.kibosh.org/pykaraoke',
  'license' : 'LGPL',
  'long_description' : 'PyKaraoke - CD+G/MPEG/KAR Karaoke Player',
  'packages':find_packages(),
  'ext_modules' : [cdgaux_ext],
  'data_files' : data_files,
  'cmdclass' : cmdclass,
  'classifiers' : [
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Games/Entertainment',
        'Topic :: Multimedia :: Sound/Audio :: Players'
        ],
  'entry_points': """\
        [console_scripts]
        pykaraoke = pykaraoke.pykaraoke:main
        pykaraoke_mini = pykaraoke.pykaraoke_mini:main
        pycdg = pykaraoke.pycdg:main
        pykar = pykaraoke.pykar:main
        pympg = pykaraoke.pympg:main
      """
  }

# Let's extend build_ext so we can allow the user to specify
# explicitly the location of the SDL installation (or we can try to
# guess where it might be.)  Also allow building of C extension to fail.
class my_build_ext(build_ext):
    user_options = build_ext.user_options
    user_options += [
        ('sdl-location=',
         None,
         "Specify the path to the SDL source directory, assuming sdl_location/include and sdl_location/lib exist beneath that.  (Otherwise, use --include-dirs and --library-dirs.)"),
        ]

    def initialize_options(self):
        build_ext.initialize_options(self)
        self.sdl_location = None

    def finalize_options(self):
        build_ext.finalize_options(self)
        
        sdl_include_paths = ['../pygame/src']
        if not windows:
            sdl_include_paths.append('/usr/include/SDL')

        if self.sdl_location is not None:
            sdl_include_paths.append(
                os.path.join(self.sdl_location, 'include')
                )

        self.include_dirs.extend(sdl_include_paths)

    def run(self):
        try:
            build_ext.run(self)
        except DistutilsPlatformError as e:
            self._unavailable(e)

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except (CCompilerError, DistutilsExecError) as e:
            self._unavailable(e)

    def _unavailable(self, e):
        print('*' * 80)
        print("""WARNING:

        An optional code optimization (C extension) could not be compiled.

        Optimizations for this package will not be available!""")
        print ('')
        print (e)
        print ('*' * 80)

cmdclass['build_ext'] = my_build_ext

setup(**setupArgs)
