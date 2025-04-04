from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme_file:
    readme = readme_file.read()

requirements = [
    "beautifulsoup4",
    "requests",
    "fuzzywuzzy",
    "python-Levenshtein"
]

setup(
    name="ProPyCore",
    version="0.5.6",
    author="Hagen E. Fritz",
    author_email="hfritz@r-o.com",
    description="Interact with Procore through Python for data connection applications",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords=['procore', 'api', 'python', 'sdk'],
    url="https://github.com/rogers-obrien-rad/ProPyCore",
    packages=find_packages(exclude=["snippets", "tests"]),
    install_requires=requirements,
    tests_require=[
        'pytest',
        'pytest-mock'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
