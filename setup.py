from setuptools import setup, find_packages
import os

here = os.path.dirname(__file__)
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='envbash',
    version='2.0.0',
    description='Source env.bash script to update environment',
    long_description=long_description,
    url='https://github.com/scampersand/envbash-python',
    author='Aron Griffis',
    author_email='aron@scampersand.com',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    keywords='bash environment environ env'.split(),
    packages=find_packages(exclude=['tests']),
    install_requires=[],
)
