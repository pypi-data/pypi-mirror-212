from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.5'
DESCRIPTION = 'Software Development Kit for Latinex (https://www.latinexbolsa.com)'
LONG_DESCRIPTION = 'This SKD facilitates the use of the Latinex REST API, it allows the user to register (getting an API Key) and to fetch data in a friction-less manner'

# Setting up
setup(
    name="latinex_sdk",
    version=VERSION,
    author="Blasser Analytica (Rodolfo Blasser)",
    author_email="<rodolfoblasser@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests', 'pandas', 'urllib3'],
    keywords=['python', 'panama', 'finance', 'stocks', 'fixed income', 'data', 'api', 'market data', 'latinex'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)