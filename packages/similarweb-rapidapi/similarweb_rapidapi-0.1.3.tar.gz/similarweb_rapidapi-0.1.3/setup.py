from setuptools import setup

setup(
    name='similarweb_rapidapi',
    version='0.1.3',
    description='SimilarWeb API on RapidAPI',
    packages=['similarweb_rapidapi', 'similarweb_rapidapi.schemas'],
    author_email='hello@letsscrape.com',
    zip_safe=False,
    author='LetsScrape',
    keywords=['rapidapi', 'similarweb', 'similarweb api', 'scraping', 'parsing', 'scraper'],
    classifiers=[],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://letsscrape.com/scrapers/similarweb-api/',
)
