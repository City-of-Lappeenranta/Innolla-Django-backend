#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# All rights reserved.
#

from setuptools import setup, find_packages

readme = open('README.rst').read()

setup(
  name='innolla',
  version='dev',
  description="""innolla""",
  long_description=readme,
  author='Haltu',
  packages=find_packages(),
  include_package_data=True,
  license="Haltu",
  zip_safe=False,
  keywords='innolla-web',
  install_requires=[
  ],
)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
