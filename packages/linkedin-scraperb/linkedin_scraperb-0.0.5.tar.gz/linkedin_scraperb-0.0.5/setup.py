from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import re

here = path.abspath(path.dirname(__file__))

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('linkedin_scraperb/__init__.py').read(),
    re.M
    ).group(1)

# Get the long description from the README file
#with open('README.md', encoding='utf-8') as f:
#    long_description = f.read()

setup( 
    name = 'linkedin_scraperb', 
    packages = ['linkedin_scraperb'], # this must be the same as the name above 
    version = version, 
    description = 'Scrapes user data from Linkedin (this is a branch)', 
    long_description = 'OK',
    long_description_content_type='text/markdown',
    author = 'Joey Sham', 
    author_email = 'sham.joey@gmail.com', 
    url = 'https://github.com/RRohjansRsm/linkedin_scraper', # use the URL to the github repo 
    download_url = 'https://github.com/RRohjansRsm/linkedin_scraper/archive/refs/tags/' + version + '.tar.gz', 
    keywords = ['linkedin', 'scraping', 'scraper'],
    classifiers = [], 
    install_requires=[
        'selenium',
        'requests',
        'lxml'
    ]
)

