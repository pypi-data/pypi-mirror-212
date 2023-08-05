
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f.readlines()]

setup(
    name="chromadb-semantic",
    version="1.0.0",
    packages=find_packages(),
    py_modules=['chromadb_semantic'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'chromadb_semantic = chromadb_semantic:main',
        ],
    },
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',)
