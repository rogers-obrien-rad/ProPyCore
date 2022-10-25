from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = [
    "beautifulsoup4==4.11.1",
    "python-dotenv==0.21.0",
    "requests==2.28.1",
    "twine==1.13.0"
]

setup(
    name="ProPyCore",
    version="0.0.1",
    author="Hagen E. Fritz",
    author_email="hagenfritz@gmail.com",
    description="Interact with Procore through Python for data connection applications",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/rogers-obrien-rad/ProPyCore",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache License 2.0"
    ]
)