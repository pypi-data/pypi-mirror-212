from setuptools import setup, find_packages
from io import open

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='semter',
    version='0.0.2',
    author='solarmar',
    author_email='maria134perminova@gmail.com',
    license='MIT',
    classifiers=classifiers,
    packages=find_packages(),
)