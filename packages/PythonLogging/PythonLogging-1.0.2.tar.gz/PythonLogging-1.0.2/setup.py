from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="PythonLogging",
    version="1.0.2",
    author="Osman TUNA",
    description="A simple logging library for easy log file management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SForces/PythonLogging",
    packages=["PythonLogging"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
