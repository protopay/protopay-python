#!/usr/bin/env python
from setuptools import setup


classifiers = ["Development Status :: 4 - Beta",
               "Environment :: Plugins",
               "Intended Audience :: Developers",
               "Programming Language :: Python",
               "Programming Language :: Python :: 2.7",
               "Programming Language :: Python :: 3",
               "Programming Language :: Python :: 3.4",
               "Programming Language :: Python :: Implementation :: PyPy",
               "License :: OSI Approved :: Apache Software License",
               "Topic :: Software Development :: Testing"]

requirements = ["requests>=2.3.0"]

setup(name='yollapay',
      version='0.0.1',
      description="",
      long_description=None,
      classifiers=classifiers,
      keywords='',
      author='',
      author_email='steve@stevepeak.net',
      url='http://github.com/yollapay/yollapay',
      packages=['yollapay'],
      include_package_data=True,
      zip_safe=True,
      install_requires=requirements,
      entry_points={'console_scripts': ['tyollapay=yollapay:main']})
