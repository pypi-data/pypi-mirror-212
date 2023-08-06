from setuptools import setup, find_packages
from torch.utils.cpp_extension import CppExtension, BuildExtension
from setuptools.command.install import install
import subprocess

VERSION = '0.0.14'
DESCRIPTION = 'A lung analysis pipeline'
LONG_DESCRIPTION = 'A lung analysis pipeline for normalization, detection, segmentation, and feature extraction'

class CustomInstallCommand(install):
    def run(self):
        # Run the default install command
        install.run(self)

        # Run the additional installation command for the extension module
        command = ['python', 'lung_analysis_pipeline/NoduleDetect_SANet/build/box/setup.py', 'install']
        result = subprocess.run(command)

        if result.returncode == 0:
            print("Additional installation successful")
        else:
            print("Additional installation failed")
            print("Error message:", result.stderr)

setup(
    name='lung_analysis_pipeline',
    version=VERSION,
    author='Olivia Zhang',
    author_email='<olivia.zhang@ucla.edu>',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    # packages=['lung_analysis_pipeline'],
    packages=find_packages(),
    install_requires=[
        'numpy==1.18.0',
        'torch',
        'bm3d',
        'nibabel',
        'tqdm',
        'pydicom',
        'termcolor',
        'ninja==1.9.0'
    ],
    cmdclass={
              'build_ext': BuildExtension},
            #   'install': CustomInstallCommand,
    ext_modules=[
        CppExtension('lung_analysis_pipeline.NoduleDetect_SANet.utils.pybox', 
        ['lung_analysis_pipeline/NoduleDetect_SANet/build/box/box.cpp'])
        # ['NoduleDetect_SANet/build/box/box.cpp'])
    ],
    include_package_data=True,
)