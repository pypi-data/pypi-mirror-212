from setuptools import setup, find_packages
from setuptools.command.install import install
import codecs
import os
import subprocess


VERSION = '0.0.8'
DESCRIPTION = 'A lung analysis pipeline'
LONG_DESCRIPTION = 'A lung analysis pipeline for normalization, detection, segmentation, and feature extraction'

class InstallLocalPackage(install):
    def run(self):
        install.run(self)
        subprocess.call(
            "python lung_analysis_pipeline/NoduleDetect_SANet/build/box/setup.py install", shell=True
        )

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
        'pydicom',
        'termcolor'
    ], 
    # include_package_data=True,
    cmdclass={ 'install': InstallLocalPackage }
)