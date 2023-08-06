The ddr-clips runtime is available from www.pypi.org: https://pypi.org/project/ddr-clips/

The ddr-clips runtime is installed by running: python3 -m pip install ddr-clips

The following modules are installed:

ddrclass - Python module containing DDR Class implementing the DDR runtime
genie_parsers - Parsing classes to convert unstructured text, CLI command/show command/log file content to Python dictionaries used to generate CLIPs FACTs
ddrrun - Python script used to execute DDR usecase
ddrparserlib - DDR functions used during testing of parsers

Update ddr-clips PyPi repository

The following modules are required to build and upload Python projects:

python3 -m pip install build
python3 -m pip install twine
python3 -m pip install wheel

To upload to PyPi you must have an account on PyPi.org

Python setup.py file
A "setup.py" file in the ddr-clips directory controls building the ddr-clips package.  The version number highlighted in red must be updated each time the package is uploaded.

The modules in the 'py_modules' list are built into the  clips installation.


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

    setuptools.setup(
        name="ddr-clips", # DDR-CLIPs runtime
        version="0.1.2", #Update the version number here
        author="Peter Van Horne",
        author_email="petervh@cisco.com",
        description="Distributed Device Reasoning (DDR) CLIPs runtime",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://wwwin-github.cisco.com/petervh/ddr-clips",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
             "Operating System :: OS Independent",
                         ],
    python_requires='>=3.6',
    py_modules=['genie_parsers', 'ddrclass', 'ddrparserlib', 'ddrrun'],
     )

Building and uploading ddr-clips
cd ddr-clips/ddr-packaging
cd dist
rm *
cd ..
python3 -m build
python3 -m twine upload --repository pypi dist/* --verbose


