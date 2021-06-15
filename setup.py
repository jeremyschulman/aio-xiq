# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["aioxiq", "aioxiq.v1", "aioxiq.v2"]

package_data = {"": ["*"]}

install_requires = ["httpx", "tenacity>=7.0.0,<8.0.0"]

setup_kwargs = {
    "name": "aio-xiq",
    "version": "0.1.0",
    "description": "AsyncIO client for Extreme Cloud IQ",
    "long_description": None,
    "author": "Jeremy Schulman",
    "author_email": "jeremy.schulman@mlb.com",
    "maintainer": None,
    "maintainer_email": None,
    "url": None,
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "python_requires": ">=3.8,<4.0",
}


setup(**setup_kwargs)
