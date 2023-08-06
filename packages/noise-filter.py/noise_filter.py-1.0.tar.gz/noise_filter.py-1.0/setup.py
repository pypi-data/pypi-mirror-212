# from distutils.core import  setup
from setuptools import setup
setup(
      name = 'noise_filter.py',
      version = '1.0',
      author = 'zyq',
      py_modules=['noise_filter.opencv_filter', 'noise_filter.PIL_filter', 'noise_filter.skimage_filter'] #记得改名字

)

