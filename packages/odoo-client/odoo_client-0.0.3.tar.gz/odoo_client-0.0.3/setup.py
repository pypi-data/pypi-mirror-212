from setuptools import setup, find_packages

VERSION = "0.0.3"
DESCRIPTION = "Simple API wrapper for Odoo's External API"
LONG_DESCRIPTION = "Simple API wrapper for Odoo's External API"

setup(
    name="odoo_client",
    version=VERSION,
    author="Michael Farwell",
    author_email="mike@lie-nielsen.com",
    url="https://github.com/LNTW/odoo-python-api",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=["python", "odoo", "api"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ]
)
