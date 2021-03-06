# -*- coding: utf-8 -*-

import sys

from setuptools import setup, find_packages


with open('VERSION.txt', 'r') as f:
    pkg_version = f.read().strip()


def get_long_description():
    with open('README.rst', 'r') as f:
        return f.read()


install_requires = [
    'PyMySQL == 0.7.11',
    'beautifulsoup4 >= 4.1.1',
    'django >= 1.11,<2.0',
    'django-contrib-comments == 1.8.0',
    'django-tinymce == 2.7.0',
    'django-uuslug == 1.1.8',
    'html2text',
    'kobo == 0.7.0',
    'odfpy >= 0.9.6',
    'python-bugzilla',
    'six',
    'xmltodict',
]

if sys.version_info.major < 3:
    install_requires += [
        'enum34',
    ]

extras_require = {
    # Required for tcms.core.contrib.auth.backends.KerberosBackend
    'krbauth': [
        'kerberos == 1.2.5'
    ],

    # Packages for building documentation
    'docs': [
        'Sphinx >= 1.1.2',
        'sphinx_rtd_theme',
    ],

    # Necessary packages for running tests
    'tests': [
        'coverage',
        'factory_boy',
        'flake8',
        'mock',
        'pytest',
        'pytest-cov',
        'pytest-django',
    ],

    # Contain tools that assists the development
    'devtools': [
        'django-debug-toolbar == 1.7',
        'tox',
        'django-extensions',
        'pygraphviz',
        'future-breakpoint',
    ],

    # Required packages required to run async tasks
    'async': [
        'celery == 4.1.0',
    ]
}


setup(
    name='Nitrate',
    version=pkg_version,
    description='Test Case Management System',
    long_description=get_long_description(),
    author='Nitrate Team',
    maintainer='Chenxiong Qi',
    maintainer_email='qcxhome@gmail.com',
    url='https://github.com/Nitrate/Nitrate/',
    license='GPLv2+',
    keywords='test case',
    install_requires=install_requires,
    extras_require=extras_require,
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
    ],
)
