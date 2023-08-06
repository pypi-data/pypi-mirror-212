from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(
    name="sabia-utils",
    version="0.2.0",
    license="MIT License",
    author="AI Lab Unb",
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email="ailabunb@gmail.com",
    keywords="sabia utils",
    description="Group of utilities for Sabia",
    packages=["sabia_utils", "sabia_utils.utils"],
    install_requires=[
        "pandas==1.4.3",
        "alei-utils==0.1.3",
        "pyarrow==6.0.1",
        "matplotlib==3.4.3",
        "scikit-learn==1.0.2",
    ],
)
