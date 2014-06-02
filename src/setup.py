from setuptools import setup,find_packages
from hammr.utils.constants import *
import os
import sys


# Declare your packages' dependencies here, for eg:
requires=['uforge_python_sdk',
                    'httplib2==0.9',
                    'cmd2==0.6.7',                    
                    'texttable==0.8.1',
                    'progressbar==2.3',
                    'argparse',
                    'paramiko==1.12',
                    'pyparsing==2.0.2',
                    'hurry.filesize==0.9',
                    'termcolor==1.1.0',
                    'junit-xml==1.3']
                    
if os.name != "nt":
	if not "linux" in sys.platform:
		#mac os
	        requires.append('readline')
else:   #On Windows
        requires.append('pyreadline==2.0')
    
                    
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
       
  
  #long_description= 'Long description of the package',
  scripts = ['bin/hammr', 'bin/hammr.bat'],
  
)
