from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

VERSION = "0.0.5"
DESCRIPTION = "Simple API wrapper for Odoo's External API"
LONG_DESCRIPTION = readme

setup(
    name="odoo_client",
    version=VERSION,
    author="Michael Farwell",
    author_email="mike@lie-nielsen.com",
    url="https://github.com/LNTW/odoo-python-api",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    license="MIT",
    keywords=["python", "odoo", "api"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ]
)
