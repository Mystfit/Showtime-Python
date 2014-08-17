from setuptools import setup, find_packages

setup(name='Showtime-Python',
      version='1.0',
      description='The ZstShowtime library is designed for live performances using ZeroMQ.',
      author='Byron Mallett',
      author_email='byronated@gmail.com',
      url='http://github.com/Mystfit/Showtime',
      license='MIT',
      install_requires=["pyzmq"],
      packages=find_packages(),
)
