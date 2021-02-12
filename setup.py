from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pfs",
    version="0.1",
    description="The library for parsing the coding problem function signature.",
    long_description=long_description,
    url="https://github.com/InterviewKickstart/ProblemFunctionSignature",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)
