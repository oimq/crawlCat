from setuptools import setup, find_packages

setup(name="crawlCat",
      version=2.0,
      url='https://github.com/oimq/crawlCat',
      author="oimq",
      author_email='taep0q@gmail.com',
      description='Crawling and scraping the web pages with selenium and chrome module',
      packages=find_packages(),
      install_requires=['selenium', 'tqdm'],
      zip_safe=False
)