"""setup"""
import pathlib
import os
import codecs
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (HERE / 'README.md').read_text(encoding='utf-8')
__version__ = '0.0.4'
__maintainer__ = 'Ujjwal Chowdhury'


# Setting up
setup(
    name='get_tense',
    version=__version__,
    description='An open-source python package to find the tense of each sentence',
    author=__maintainer__,
    author_email='<u77w41@gmail.com>',
    url='https://github.com/U77w41/',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data = True,
    data_files=[
        ('get_tense',['get_tense/past_tense_verbs']),
    ],
    install_requires=['nltk','regex','pathlib'],
    tests_require=['pytest'],
    keywords= ['python','text','regex', 'tense classification','grammer']
)

#################################################################################################################
# python3 setup.py sdist bdist_wheel
# twine upload dist/*