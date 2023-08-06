from setuptools import setup, find_packages

VERSION = '0.1.1'
DESCRIPTION = "Package providing functional error handling."
LONG_DESCRIPTION = "Package provinding functional error handling in 'monadic'-like way. Allows you to create wrapped value from success value or an error, apply functions to wrapped value and unwrap."

setup(
    name="pyerr",
    version=VERSION,
    author="Vojtech Soukenka",
    author_email="<vojtech.soukenka@gmail.com>",
    url="https://github.com/soukev/pyerr",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages= find_packages(),
    install_requires=[],
    keywords=['error', 'error handling', 'functional'],
    classifiers= [
        "Intended Audience :: Developers",
        "Programming Language :: Python"
    ]
)
