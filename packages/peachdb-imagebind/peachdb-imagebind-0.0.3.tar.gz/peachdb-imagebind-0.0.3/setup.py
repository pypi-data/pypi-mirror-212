from setuptools import find_packages, setup

requirements = []

# Read requirements from files
with open("requirements.txt", "r") as f:
    requirements.extend(f.read().splitlines())

setup(
    name="peachdb-imagebind",
    version="0.0.3",
    packages=find_packages(),
    package_data={"imagebind": ["bpe/bpe_simple_vocab_16e6.txt.gz"]},
    install_requires=requirements,
    dependency_links=["https://download.pytorch.org/whl/cu113"],
)
