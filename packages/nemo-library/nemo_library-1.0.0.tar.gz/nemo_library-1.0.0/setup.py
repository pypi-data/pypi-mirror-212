from setuptools import setup, find_packages

setup(
    name='nemo_library',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests','pandas'
    ],
    author='Gunnar Schug',
    author_email='GunnarSchug81@gmail.com',
    description='A library for uploading data to and downloading reports from NEMO cloud solution',
    classifiers=[
        'Programming Language :: Python :: 3.11',
    ],
)
