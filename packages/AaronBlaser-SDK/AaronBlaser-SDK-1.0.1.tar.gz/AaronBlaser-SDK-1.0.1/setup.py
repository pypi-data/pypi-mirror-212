from setuptools import setup, find_packages

setup(
    name="AaronBlaser-SDK",
    version="1.0.1",
    author="Aaron Blaser",
    author_email="ablaser5@comcast.net",
    description="SDK for the lord of the rings API",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ablaser5/AaronBlaser-SDK",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=[
        "certifi==2023.5.7",
        "charset-normalizer==3.1.0",
        "idna==3.4",
        "requests==2.31.0",
        "urllib3==2.0.2",
    ],
)