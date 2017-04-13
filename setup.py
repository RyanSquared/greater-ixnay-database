#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='Greater Ixnay Database',
    version='0.1.0-1',
    description='Database for information over the Greater Ixnay geographical'
    + 'and political regions',
    requires=['flask', 'tornado'],
    author='Ryan',
    author_email='vandor2012@gmail.com',
    url='https://github.com/RyanSquared/greater-ixnay-database',
    packages=['gixnaydb'])
