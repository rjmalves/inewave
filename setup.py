from setuptools import setup, find_packages  # type: ignore

long_description = ""
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = []
with open('requirements.txt', 'r') as fh:
    requirements = fh.readlines()

setup(
    name="inewave",
    version_config=True,
    setup_requires=['setuptools-git-versioning'],
    author="Rogerio Alves",
    author_email="rogerioalves.ee@gmail.com",
    description="Interface para arquivos do NEWAVE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rjmalves/inewave",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning"
    ],
    python_requires=">=3.6",
    install_requires=requirements
)
