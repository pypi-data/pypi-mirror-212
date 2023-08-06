import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ericstools",
    version="0.0.1",
    author="Eric Schmidt",
    author_email="eric_schmidt_99@gmx.de",
    description="Tools that I use daily.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/Nablaaa/ericstools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
        "hydra-core",
        "scikit-image",
        "pandas",
    ],
    include_package_data=True,
)
