from setuptools import setup

setup(
    name='fetch-lyrics-from-genius',
    version='0.1.1',
    description='A package to fetch lyrics from Genius.com',
    author='Andrew Beveridge',
    author_email='andrew@beveridge.uk',
    packages=['fetch_lyrics_from_genius'],
    install_requires=[
        'lyricsgenius',
        'musicbrainzngs',
        'python-slugify'
    ],
    entry_points={
        'console_scripts': [
            'fetch-lyrics-from-genius = fetch_lyrics_from_genius.fetch_lyrics:main',
        ],
    },
)
