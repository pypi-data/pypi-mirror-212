"""This module contains a Zope product for an ordered btree folder."""

from setuptools import find_packages
from setuptools import setup
import os


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read() + '\n\n'


version = '3.2'

long_description = (
    '.. contents ::\n\n' +
    read('CHANGES.rst') +
    read('src', 'Products', 'orderedbtreefolder', 'README.rst')
)

tests_require = ['zope.testing >= 3.8']

setup(name='Products.orderedbtreefolder',
      version=version,
      description=(
          "BTree folder with the option to keep an ordering in the items"),
      long_description=long_description,
      classifiers=[
          "Framework :: Zope :: 4",
          "Framework :: Zope :: 5",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
          "Programming Language :: Python :: Implementation :: CPython",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Development Status :: 5 - Production/Stable",
      ],
      keywords='union.cms zope python content',
      author='union.cms developers',
      author_email='dev@unioncms.org',
      url='https://gitlab.com/gocept/union.cms/products.orderedbtreefolder',
      license='GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      python_requires='>=3.7, <4',
      install_requires=[
          'AccessControl',
          'Acquisition',
          'Products.BTreeFolder2 >= 4',
          'Products.ZCatalog',
          'ZODB',
          'Zope >= 4.0b7',
          'setuptools',
          'zExceptions',
      ],
      tests_require=tests_require,
      extras_require=dict(test=tests_require),
      test_suite='Products.orderedbtreefolder.tests',
      )
