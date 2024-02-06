# Project Python Cellular Automata

# PyAnnealing Setup

# Python Modules
from setuptools import setup, find_packages

# Local Modules
from pyannealing.version import VERSION

DESCRIPTION = 'Python Simulated Annealing',
# LONG_DESCRIPTION = DESCRIPTION

# with open('README.md', 'r', encoding='utf-8') as readme:
#     LONG_DESCRIPTION = readme.read()

setup(
    name='PyAnnealing',
    author='Michael Buckley',
    description=DESCRIPTION,
    # long_description=LONG_DESCRIPTION,
    # long_description_content_type = 'text/markdown',
    version=VERSION,
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib'
    ],
    keywords=['simulated annealing']
)