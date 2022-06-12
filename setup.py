import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="pgnhelper",
    version='0.1.14',
    author='Ferdinand Mosca',
    author_email="ferdymosca@gmail.com",
    description="An application to process pgn file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fsmosca/pgnhelper",
    project_urls={
        "Bug Tracker": "https://github.com/fsmosca/pgnhelper/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
          'chess==1.9.1',
    ]
)