import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="akms-hash",
    version="0.4.0",
    author="apinanyogaratnam",
    author_email="apinanapinan@icloud.com",
    description="An API Key hashing library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/apinanyogaratnam/akms-hash",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[],
)
