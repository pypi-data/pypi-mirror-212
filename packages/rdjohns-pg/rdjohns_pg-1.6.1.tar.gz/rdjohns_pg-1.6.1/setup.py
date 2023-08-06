import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rdjohns_pg",
    version="1.6.1",
    author="David Johns",
    author_email="rakotonindrianajohns@email.com",
    description="Use for the multiple delete, update or insert and select!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RDJohns/rdjohns_pg",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
# Create your Distribution Archive Files
#-------------------------------------------------
# pip3 install  setuptools wheel 
# python setup.py sdist bdist_wheel

# Upload your distribution archives to PyPI
#-------------------------------------------------
# pip3 install twine 
# twine upload dist/* 

# Test Your New Package
#-------------------------------------------------
# pip install rdjohns-pg