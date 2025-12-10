#!/usr/bin/env python3
"""
Setup configuration for q2bs-auditor package.

This enables pip installation and distribution via PyPI.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="q2bs-auditor",
    version="1.0.0",
    author="Anthony CHARRETIER",
    author_email="contact@anthony-charretier.fr",
    description="Forensic analysis tool for documenting industrial-scale automated content generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/innermost47/q2bs",
    project_urls={
        "Bug Reports": "https://github.com/innermost47/q2bs/issues",
        "Source": "https://github.com/innermost47/q2bs",
        "Case Study": "https://dev.to/innermost_47/when-ai-content-systems-reproduce-content-without-attribution-a-documented-case-study-1h0g",
    },
    packages=find_packages(),
    py_modules=[
        'run',
        'q2b_studio_auditor',
        'q2b_data_visualizer',
        'wayback_archiver',
        'similarity_analyzer',
        'dashboard',
        'main',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "matplotlib>=3.7.0",
        "streamlit>=1.28.0",
        "plotly>=5.17.0",
        "pandas>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "q2bs-audit=run:main",
            "q2bs-similarity=similarity_analyzer:main",
            "q2bs-dashboard=dashboard:main",
        ],
    },
    keywords=[
        "plagiarism",
        "content-analysis",
        "web-scraping",
        "journalism",
        "forensics",
        "ai-content",
        "automated-content",
        "industrial-scale",
    ],
    include_package_data=True,
    zip_safe=False,
)
