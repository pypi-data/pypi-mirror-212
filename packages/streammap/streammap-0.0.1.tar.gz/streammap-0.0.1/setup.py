import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'streammap',
    version = '0.0.1',
    author = 'Yassine Hammoud',
    author_email = 'yassinehammoud@geo-ap.com',
    description = 'An automated river analysis and mapping engine.',
    keywords = 'remote sensing, stream, satellite, river',
    url = 'https://github.com/geoapnet/streammap',
    long_description = read('README.md'),  # Assuming you have a README file
    long_description_content_type = 'text/markdown',  # Specify the README file type
    classifiers = [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    package_dir={'streammap': 'src/streammap'},
    install_requires = [
        'numpy',
        'scipy',
        'matplotlib',
        'gdal',
        'opencv-python',
        'pyshp'
    ],
)
