from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Command analyzer for pandas first version and it has assistant its will be cool'

# Setting up
setup(
    name="gnlib",
    version=VERSION,
    author="sliwGN team",
    author_email="giokhvichia69@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "nltk",
        "pandas",
        "pyttsx3",
        "speechrecognition"
    ],
    keywords=['python', 'data', 'analyze', 'information', "simplicity", "assistant"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
