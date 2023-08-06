import os
import sys
import platform
import distutils.command.build as _build
from distutils import spawn
from distutils.sysconfig import get_python_lib
from setuptools import setup, find_packages


def check_requirements():
    """Check if the system requirements are met."""
    # Check the operating system
    os_name = platform.system()
    if os_name not in ['Darwin', 'Linux']:
        sys.stderr.write(
            "Unsupported operating system. Please use MacOS or Linux.\n")
        return False

    # Check the Python version
    if sys.version_info < (3, 6):
        sys.stderr.write("Python 3.6 or higher is required.\n")
        return False

    # For Mac, min is Python3.8
    if sys.version_info < (3, 8) and os_name == 'Darwin':
        sys.stderr.write("Python 3.8 or higher is required.\n")

    return True


# If the system does not meet requirement, exit.
if not check_requirements():
    sys.exit(1)

_here = os.path.abspath(os.path.dirname(__file__))
version = {}
with open(os.path.join(_here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pydisort',
    version='0.0.6',
    description='Modern Python interfaces of DISORT.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Zoey Hu',
    author_email='zoey.zyhu@gmail.com',
    packages=find_packages(),
    package_data={'pydisort': ['*.so*', '*.toml*']},  # Include the .so file
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3 :: Only'
    ],
    python_requires=">=3.6"
)
