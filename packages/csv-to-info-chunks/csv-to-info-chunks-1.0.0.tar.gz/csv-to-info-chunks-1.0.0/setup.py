
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f.readlines()]

setup(
    name="csv-to-info-chunks",
    version="1.0.0",
    packages=find_packages(),
    py_modules=['csv_to_info_chunks'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'csv_to_info_chunks = csv_to_info_chunks:main',
        ],
    },
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',)
