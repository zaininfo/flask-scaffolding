# -*- coding: utf8 -*-

from setuptools import setup, find_packages

from scaffolding import __version__

with open('README.md', 'r') as f:
    README = f.read()

with open('requirements.txt', 'r') as f:
    INSTALL_REQUIREMENTS = f.read().splitlines()

setup(
    name='scaffolding',
    version=__version__,
    description='A scaffolding for a Flask project.',
    long_description=README,
    url='',
    author='Zain ul Abideen',
    author_email='',
    license='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: ',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic ::  :: '
    ],
    keywords='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=INSTALL_REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'scaffolding=scaffolding.runner:run'
        ]
    }
)
