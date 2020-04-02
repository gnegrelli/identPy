from setuptools import setup, find_packages

setup(
    name='identpy',
    version='1.0.0',
    packages=find_packages(),
    author='Gabriel Negrelli',
    author_email='gabriel.jose.gomes@usp.br',
    description='identPy - A tool for parameter estimation of mathematical models',
    install_requires=[
        'numpy==1.17.4',
        'scipy==1.4.1',
        'matplotlib==3.1.2',
    ],
)