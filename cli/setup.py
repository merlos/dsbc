#!/usr/bin/env python3
from setuptools import setup, find_packages
import os

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read version from package
def get_version():
    """Read version from __init__.py or use default."""
    try:
        with open("deepseek_balance/__init__.py", "r") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return "1.0.0"

setup(
    name="dsbc",
    version=get_version(),
    author="Merlos",
    author_email="merlos@users.github.com",
    description="DeepSeek Balance Checker - CLI tool to check DeepSeek API account balances",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/merlos/dsbc",
    packages=find_packages(include=["deepseek_balance", "deepseek_balance.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "rich>=13.0.0",  # For pretty output
        "typer>=0.9.0",  # For better CLI experience
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "isort>=5.12.0",
            "twine>=4.0.0",
            "build>=1.0.0",
        ],
        "uv": [
            "uv>=0.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "dsbc=deepseek_balance.cli:main",
        ],
    },
    include_package_data=True,
    keywords="deepseek, api, balance, cli, tool, ai, llm",
    project_urls={
        "Bug Reports": "https://github.com/merlos/dsbc/issues",
        "Source": "https://github.com/merlos/dsbc",
        "Documentation": "https://github.com/merlos/dsbc#readme",
    },
)