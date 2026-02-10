#!/usr/bin/env python3
"""
Setup script for Lume Security Toolkit
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="lume-security-toolkit",
    version="0.3.0",
    author="Lume Security Team",
    author_email="security@lume.dev",
    description="Think in English. Hack in Kali. - Natural language pentesting CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/lume-security-toolkit",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'lume': ['data/*.json'],
    },
    entry_points={
        'console_scripts': [
            'lume=lume.cli:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Core dependencies (none for basic operation)
    ],
    extras_require={
        'ml': [
            'spacy>=3.0.0,<4.0.0',
        ],
    },
    keywords="pentesting security kali-linux cybersecurity ethical-hacking cli machine-learning nlp",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/lume-security-toolkit/issues",
        "Source": "https://github.com/yourusername/lume-security-toolkit",
        "Documentation": "https://github.com/yourusername/lume-security-toolkit/wiki",
    },
)
