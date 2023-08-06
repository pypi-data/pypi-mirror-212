from setuptools import setup, find_packages

# Package metadata
name = "LockAPI"
version = "1.0.0"
description = "A package for creating and managing locks"
long_description = "A client and server implementation for managing locks using a REST API."
author = "Aleph Firmino"
author_email = "alephfirmino@protonmail.com"
url = ""
license = "MIT"

# Required packages
install_requires = [
    "httpx",
    "aiohttp",
]

# Find packages
packages = find_packages()

# Setup function call
setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    install_requires=install_requires,
    packages=packages,
)