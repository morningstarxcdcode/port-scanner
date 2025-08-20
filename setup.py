from setuptools import setup, find_packages # type: ignore

setup(
    name="advanced-port-scanner",
    version="1.0.0",
    description="A highly advanced modular port scanner and wireless attack tool",
    author="morningstarxcdcode",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "python-nmap>=0.7.1",
        "requests>=2.31.0",
        "shodan>=1.31.0",
        "fpdf2>=2.7.4",
        "pandas>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "advportscan=main:main",
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
