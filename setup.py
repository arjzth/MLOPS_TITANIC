from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="MLOPS-Titanic",
    version="0.1",
    author="Arjun",
    packages=find_packages(),
    install_requires=requirements,
)