from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'Command analyzer for pandas new version'

# Setting up
setup(
    name="sliw",
    version=VERSION,
    author="sliw team",
    author_email="giokhvichia69@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/plain",
    packages=find_packages(),
    install_requires=[
        "nltk",
        "pandas"
    ],
    keywords=['python', 'data', 'analyze', 'information', "simplicity"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
