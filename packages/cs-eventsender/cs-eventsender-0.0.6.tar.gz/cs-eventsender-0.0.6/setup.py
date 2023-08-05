from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.6'
DESCRIPTION = 'A package for sending event notifications.'
LONG_DESCRIPTION = 'A package for sending event notifications.'

# Setting up
setup(
    name="cs-eventsender",
    version=VERSION,
    author="Richard",
    author_email="<rich_swainson@hotmail.co.uk>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests','cs-telegram-bot-api'],
    keywords=['binance', 'api', 'wrapper', 'c2c', 'sapi'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)