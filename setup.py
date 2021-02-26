from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ik.problem.function",
    version="0.1",
    description="The library for parsing the coding problem function signature.",
    long_description=long_description,
    url="https://github.com/InterviewKickstart/ProblemFunctionSignature",
    packages=['ik.problem.function'],
    package_dir={'ik.problem.function': 'src'},
)
