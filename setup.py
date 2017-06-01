from distutils.core import setup
from setuptools import setup
import panda

VERSION = 1.13

setup(
    name='ndd-panda',
    packages=[
        'panda',
        'panda.methods',
        'panda.utils',
        'panda.bench'
    ],
    scripts = [
        'panda/scripts/panda_pipeline'
    ],
    version=VERSION,
    description='Neuro Data Design EEG Preprocessing Pipeline',
    author='Ryan Marren and Nitin Kumar',
    author_email='rmarren1@jhu.edu, nkumarcc@gmail.com',
    url='https://github.com/NeuroDataDesign/orange-panda',
    keywords=[
        'eeg',
        'pipeline'
    ],
    classifiers=[],
    install_requires=[  # We didnt put versions for numpy, scipy, b/c travis-ci
        'numpy',  # We use nump v1.10.4
        'scipy',  # We use 0.17.0
        'seaborn',
        'pywavelets',
        'boto3',
        'matplotlib',
    ]
)
