from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.6'
DESCRIPTION = 'A lung analysis pipeline'
LONG_DESCRIPTION = 'A lung analysis pipeline for normalization, detection, segmentation, and feature extraction'

# Setting up
setup(
    name="lung_analysis_pipeline",
    version=VERSION,
    author="Olivia Zhang",
    author_email="<olivia.zhang@ucla.edu>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'numpy==1.18.0',
        'torch', 
        'bm3d', 
        'nibabel', 
        'tqdm', 
        'pydicom'
    ], 
    # include_package_data=True,
)