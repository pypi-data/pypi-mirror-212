from setuptools import setup, find_packages

setup(
    name='KraitUtilities',
    version='1.0.0',
    description='A package for data preprocessing and visualization',
    author='Declan van den Hoek',
    author_email='declanvandenhoek@gmail.com',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'numpy',
        'seaborn',
        'pandas',
    ],
)

