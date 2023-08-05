from setuptools import setup

setup(
    name='airtable_view_fetcher',
    version='0.2.0',
    description='Tool to scrape data from an Airtable shared view',
    url='https://github.com/vartur/airtable_view_fetcher',
    author='Vincent Artur',
    author_email='6145191+vartur@users.noreply.github.com',
    packages=['airtable_view_fetcher'],
    install_requires=[
        'requests',
        'pytz'
    ],
    entry_points={
        'console_scripts': [
            'airtable_view_fetcher=airtable_view_fetcher.fetch_airtable_data:main'
        ]
    },
    long_description_content_type='text/markdown',
    long_description='Tool to scrape data from an Airtable shared view'
)
