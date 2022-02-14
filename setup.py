import re

from setuptools import setup

with open("discode/__init__.py") as file:
    version = re.search(
        r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read(), re.MULTILINE
    ).group(1)

with open("README.md") as readme:
    readme = readme.read()

with open("requirements.txt") as req:
    requirements = req.read().splitlines()

packages = ("discode", "discode.commands")

classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Operating System :: OS Independent",
    "Topic :: Internet",
    "Topic :: Utilities",
]

setup(
    name="Discode.py",
    author="TheFarGG",
    maintainer=", ".join(["TheFarGG"]),
    url="https://github.com/thefargg/discode",
    version=version,
    packages=packages,
    license="MIT",
    description="Asynchronous Python API wrapper for the Discord Gateway API and Discord REST API.",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    extras_require={"docs": ["sphinx", "furo"]},
    python_requires=">=3.7.0",
    classifiers=classifiers,
    keywords="Discode, discode, Discord, discord",
)
