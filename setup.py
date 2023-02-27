#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Lightsong",
    author_email='qsfan@qq.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Based on Alchemy, providing crud API for table operation.",
    entry_points={
        'console_scripts': [
            'sqlalchemy_cruder=sqlalchemy_cruder.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='sqlalchemy_cruder',
    name='sqlalchemy_cruder',
    packages=find_packages(include=['sqlalchemy_cruder', 'sqlalchemy_cruder.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/fanqingsong/sqlalchemy_cruder',
    version='0.1.0',
    zip_safe=False,
)
