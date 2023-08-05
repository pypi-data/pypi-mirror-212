# setup.py
from setuptools import setup

setup(
    name="d2y",
    version="0.0.2",
    description="A Python SDK for the D2Y Exchange API",
    author="d2y Core Team",
    author_email="admin@d2y.exchange",
    url="",
    packages=['d2y'],
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
)
