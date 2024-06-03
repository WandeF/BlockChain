from setuptools import setup, find_packages

setup(
    name='blockchain',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'filelock==3.14.0',
        'lib==4.0.0',
        'PyYAML==5.4.1',
    ],
    entry_points={
        'console_scripts': [
            'blockchain = main:run',
        ],
    },
)
