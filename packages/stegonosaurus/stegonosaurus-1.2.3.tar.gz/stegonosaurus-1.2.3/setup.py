'''Setup file'''
from setuptools import find_packages, setup

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
    name='stegonosaurus',
    packages=find_packages(include=["stegonosaurus"]),
    version='1.2.3',
    description='Stegonography utilities',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Geada734',
    license='MIT',
    classifiers=classifiers,
    keywords='steganography',
    url='https://github.com/Geada734/stegonosaurus',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests'
)
