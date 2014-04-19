#!/usr/bin/env python3

import setuptools


setuptools.setup(
    name='InsightBlackjack',
    description='Simple text-based blackjack card game',
    author='Yoann Aubineau',
    author_email='yoann.aubineau@gmail.com',
    packages=['blackjack'],
    test_suite='blackjack.tests',
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Development Status :: 3 - Alpha',
    ],
)

