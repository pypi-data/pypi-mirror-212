import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="tensoract",
    version="1.0.3",
    author="Tensoract Inc.",
    author_email="support@tensoract.com",
    description="Python api client - https://api.tensoract.com/docs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deepalirajale/newton-api",
    project_urls={
        "Bug Tracker": "https://github.com/deepalirajale/newton-api/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)