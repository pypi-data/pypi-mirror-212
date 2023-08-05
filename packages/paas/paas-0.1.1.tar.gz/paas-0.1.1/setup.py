import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="paas",
    version="0.1.1",
    description="Prediction as a Service.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liaoyuhua/paas",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[],
)
