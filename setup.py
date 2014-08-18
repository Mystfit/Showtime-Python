import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='Showtime-Python',
      version='1.0.2',
      description='Showtime-Python allows you to connect multiple programs together for live performances using nodes.',
      long_description=read('README.md'),
      author='Byron Mallett',
      author_email='byronated@gmail.com',
      url='http://github.com/Mystfit/Showtime',
      license='MIT',
      install_requires=["pyzmq==14.3.1"],
      packages=find_packages(),
      classifiers=[
      'Development Status :: 4 - Beta',
      'License :: OSI Approved :: MIT License',
      'Operating System :: Microsoft :: Windows :: Windows 7',
      'Operating System :: MacOS :: MacOS X',
      'Operating System :: OS Independent',
      'Environment :: Console',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3.3',
      'Programming Language :: C#',
      'Programming Language :: Java',
      'Topic :: Software Development :: Libraries :: Python Modules',
      'Topic :: Software Development :: Object Brokering',
      'Intended Audience :: Developers',
	  'Natural Language :: English'
      ],
      scripts=['scripts/showtime-stage.py']
      )
