#! /usr/bin/env python
"""Flow cytometry for sk-learn"""

import codecs
import os

from setuptools import find_packages, setup, dist

dist.Distribution().fetch_build_eggs(['numpy>=1.19'])
import numpy as np

# get __version__ from _version.py
ver_file = os.path.join('skcyto', '_version.py')
__version__ = None
with open(ver_file) as f:
    exec(f.read())

if __version__ is None:
    raise RuntimeError("__version__ string not found in file %s" % ver_file)

DISTNAME = 'skcyto'
DESCRIPTION = '"Flow cytometry for sk-learn'
with codecs.open('README.rst', encoding='utf-8-sig') as f:
    LONG_DESCRIPTION = f.read()
MAINTAINER = 'Martin Helm'
MAINTAINER_EMAIL = 'martin@bio-ai.org'
URL = 'https://github.com/MSHelm/skcyto'
LICENSE = 'new BSD'
DOWNLOAD_URL = 'https://github.com/MSHelm/skcyto'
VERSION = __version__
INSTALL_REQUIRES = ['numpy', 'scipy', 'scikit-learn>=1.2.0', 'minisom', 'igraph', 'flowutils']
EXTRAS_REQUIRE = {
    'tests': [
        'pytest',
        'pytest-cov'
    ],
    'dev': [
        'pylint',
        'pandas'
    ],
    'docs': [
        'sphinx',
        'sphinx-gallery',
        'sphinx_rtd_theme',
        'numpydoc',
        'matplotlib'
    ]
}

setup(name=DISTNAME,
      maintainer=MAINTAINER,
      maintainer_email=MAINTAINER_EMAIL,
      description=DESCRIPTION,
      license=LICENSE,
      url=URL,
      version=VERSION,
      download_url=DOWNLOAD_URL,
      long_description=LONG_DESCRIPTION,
      zip_safe=False,  # the package can run out of an .egg file
      packages=find_packages(),
      install_requires=INSTALL_REQUIRES,
      extras_require=EXTRAS_REQUIRE)
