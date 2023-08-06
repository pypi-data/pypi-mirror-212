import setuptools
import os
from distutils.util import convert_path
from pathlib import Path

ver_path = convert_path('version.txt')
ver = None
if os.path.exists(ver_path):
    with open(ver_path) as ver_file:
        ver = ver_file.read()

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="numerous-solver",
    version=ver,
    author='Tobias Dokkedal Elmoee, EnergyMachines ApS',
    author_email='tobias.dokkedal.elmoe@energymachines.com',
    description="Numerous ODE solver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numba>=0.56.4",
        "scipy>=1.7.1",
        "Deprecated>=1.2.13"
    ],
    packages=setuptools.find_namespace_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires='>=3.10',

)
