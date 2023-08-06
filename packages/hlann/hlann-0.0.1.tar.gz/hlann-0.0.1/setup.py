from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("requirements.txt") as requirements_file:
    requirements = requirements_file.read().split("\n")

# with open("requirements-tests.txt") as requirements_file:
#     test_requirements = requirements_file.read().split("\n")

# Setting up
setup(
    name="hlann", 
    version='0.0.1' ,
    author="NMDP Bioinformatics",
    author_email="<rsajulga@nmdp.org>",
    description='HLA Annotation (HLAnn) Python package for annotating HLA',
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=[
        "hlann"
    ],
    provides=["hlann"],
    install_requires=requirements,
    license="LGPL 3.0",
    keywords='hlann',
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    test_suite="test",
    include_package_data=True
)