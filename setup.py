from setuptools import setup, find_packages

setup(
    name='identpy',
    version='1.0.0',
    packages=find_packages(exclude=('tests',)),
    author='Gabriel Negrelli',
    author_email='gnegrelli13@gmail.com',
    description='identPy - A tool for parameter estimation of mathematical models',
    install_requires=[
        'blinker==1.4',
        'numpy==1.17.4',
        'scipy==1.10.0',
        'matplotlib==3.1.2',
    ],
)
