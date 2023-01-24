import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="pgnhelper",
    version='0.10.2',
    author='Ferdinand Mosca',
    author_email="ferdymosca@gmail.com",
    description="It sorts games by tags, add eco, opening and variation and generate round-robin result table.",
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
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
          'chess==1.9.1',
          'pandas',
          'pytest'
    ],
    entry_points={
        'console_scripts': [
            'pgnhelper = pgnhelper:main',
        ]
    }
)