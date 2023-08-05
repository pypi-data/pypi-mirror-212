from setuptools import setup, find_packages

def README():
    with open("README.md", "r") as file:
        return file.read()

setup(
    name = "PixID",
    version = "1.0.0",
    author = "ttwiz_z",
    author_email = "moderkascriptsltd@gmail.com",
    description = "Generates a unique identifier for the computer.",
    long_description = README(),
    long_description_content_type = "text/markdown",
    url = "https://github.com/ttwizz",
    packages = find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    keywords = "PixID",
    project_urls = {
        "Organization": "https://github.com/ModerkaScripts"
    },
    python_requires = ">=3.8"
)