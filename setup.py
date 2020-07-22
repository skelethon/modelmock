#!/usr/bin/env python

import os
import setuptools

setup_args = dict(
  name = 'modelmock',
  version = os.environ.get('MODELMOCK_VERSION', '0.1.2'),
  description = 'A simple mock model generator',
  author = 'acegik',
  license = 'GPL-3.0',
  url = 'https://github.com/acegik/modelmock',
  download_url = 'https://github.com/acegik/modelmock/downloads',
  keywords = ['mock', 'model', 'jsonschema'],
  classifiers = [],
  install_requires = open("requirements.txt").readlines(),
  python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
  package_dir = {'':'lib'},
  packages = setuptools.find_packages('lib'),
)

if 'MODELMOCK_PRE_RELEASE' in os.environ:
  setup_args['version'] = setup_args['version'] + os.environ['MODELMOCK_PRE_RELEASE']

if __name__ == "__main__":
  setuptools.setup(**setup_args)
