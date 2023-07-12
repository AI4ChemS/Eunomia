#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()


requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    author="Mehrad Ansari",
    author_email='mehrad.ans@gmail.com',
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
    description="LLM-based tool for predicting stability of metal organic frameworks",
    install_requires=requirements,
    license="MIT license",
    include_package_data=True,
    keywords='eunomia',
    name='eunomia',
    packages=find_packages(include=['eunomia', 'eunomia.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/AI4ChemS/Eunomia',
    version='0.1.0',
    zip_safe=False,
)
