# Copyright 2007-2015 UShareSoft SAS, All rights reserved
#
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from setuptools import setup,find_packages,Command
from hammr.utils.constants import *
import os


ROOT_DIR = os.path.dirname(os.path.realpath(__file__))


# Declare your packages' dependencies here, for eg:
# Always put an '==' dependency with uforge_python_sdk
requires=['uforge_python_sdk==3.7.8',
                    'httplib2==0.9',
                    'texttable>=0.8.1',
                    'progressbar==2.3',
                    'argparse',
                    'paramiko==1.12',
                    'pyparsing==2.0.2',
                    'pyyaml==3.12',
                    'hurry.filesize==0.9',
                    'termcolor==1.1.0',
                    'junit-xml==1.3',
                    'xmlrunner==1.7.7',
                    'ussclicore==1.0.10']

test_requires=['mock']


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        os.system('rm -vrf '+ROOT_DIR+'/build '+ROOT_DIR+'/dist '+ROOT_DIR+'/*.pyc '+ROOT_DIR+'/*.egg-info')
        os.system('find '+ROOT_DIR+' -iname "*.pyc" -exec rm {} +')

setup (  

  install_requires=requires,
  tests_require = test_requires,
  
  # Fill in these to make your Egg ready for upload to
  # PyPI
  name = 'hammr',
  version = VERSION,
  description='Command-line tool for building conistent and repeatable machine images for multiple cloud platforms',
  long_description='command-line tool for building/publishing/migrating consistent machine images for virtual datacenters and cloud platforms',
  packages = find_packages(),
  author = 'Joris Bremond',
  author_email = 'joris.bremond@usharesoft.com',
  license="Apache License 2.0",
  url = 'http://hammr.io',
  classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),
       
  # ... custom build command
    cmdclass={
        'clean': CleanCommand,
    },

  #long_description= 'Long description of the package',
  scripts = ['bin/hammr', 'bin/hammr.bat'],
  
)
