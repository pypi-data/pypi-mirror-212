#!/usr/bin/python3

import os
import re

from setuptools import find_packages
from setuptools import setup

NAME =               'python-pdfbox-v2'
VERSION =            '2.0.28.3'
AUTHOR =             'Fakabbir Amin'
AUTHOR_EMAIL =       'f4amin@gmail.com'
URL =                'https://github.com/py-hacks/python-pdfbox'
DESCRIPTION =        'Python interface to Apache PDFBox command-line tools.'
with open('README.rst', 'r') as f:
    LONG_DESCRIPTION = f.read()
LONG_DESCRIPTION = re.search('.*(^Package Description.*)', LONG_DESCRIPTION, re.MULTILINE|re.DOTALL).group(1)
DOWNLOAD_URL =       URL
LICENSE =            'Apache'
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development']
PACKAGES =           find_packages()

if __name__ == "__main__":
    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    setup(
        name = NAME,
        version = VERSION,
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        license = LICENSE,
        classifiers = CLASSIFIERS,
        description = DESCRIPTION,
        long_description = LONG_DESCRIPTION,
        url = URL,
        packages = find_packages(),
        include_package_data=True,
	    python_requires='>=3',
        install_requires = ['jpype1', 'setuptools'])
