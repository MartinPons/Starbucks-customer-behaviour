from setuptools import setup, find_packages

setup(
    name='StarbucksAnalysis',
    version='0.1.0',
    description='A collection of functions and classes to analyze the Starbucks simulated dataset',
    author='My Name',
    author_email='martinpons10218@gmail.com.com',
    url='https://github.com/myusername/my_package',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'pandas'
    ])