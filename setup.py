import setuptools
from setuptools import version

long_description = ""
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="inewave",
    version="0.0.1",
    author="Rogerio Alves",
    author_email="rogerioalves.ee@gmail.com",
    description="Interface para arquivos do NEWAVE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rjmalves/inewave",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning"
    ],
    python_requires=">=3.6"
)