import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="gsaiortc",
    version="0.0.1",
    description="gsaiortc",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://glass-sphere-ai.de",
    author="Glass Sphere Software",
    author_email="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["src"],
    include_package_data=True,
    install_requires=[
        "aioice>=0.9.0,<1.0.0",
        "av>=9.0.0,<11.0.0",
        "cffi>=1.0.0",
        "cryptography>=2.2",
        'dataclasses; python_version < "3.7"',
        "google-crc32c>=1.1",
        "pyee>=9.0.0",
        "pylibsrtp>=0.5.6",
        "pyopenssl>=23.1.0",
                      ],
    entry_points={
        "console_scripts": [
            "realpython=aiortc.__main__:main",
        ]
    },
)
