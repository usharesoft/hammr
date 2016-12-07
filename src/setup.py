from setuptools import setup,find_packages, Command
from hammr.utils.constants import *
import os
import sys


ROOT_DIR = os.path.dirname(os.path.realpath(__file__))


# Declare your packages' dependencies here, for eg:
requires=['uforge_python_sdk>=3.5.1.4, <3.6',
                    'cmd2==0.6.7',                    
                    'texttable>=0.8.1',
                    'progressbar==2.3',
                    'argparse',
                    'paramiko==1.12',
                    'pyparsing==2.0.2',
                    'hurry.filesize==0.9',
                    'termcolor==1.1.0',
                    'junit-xml==1.3',
                    'xmlrunner==1.7.7']
                    
if os.name != "nt":
	if not "linux" in sys.platform:
		#mac os
	        requires.append('readline')
else:   #On Windows
        requires.append('pyreadline==2.0')

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
