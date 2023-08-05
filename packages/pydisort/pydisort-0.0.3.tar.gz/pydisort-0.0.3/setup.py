from setuptools import setup, find_packages

setup(
    name='pydisort',
    version='0.0.3',
    packages=find_packages(),
    package_data={'pydisort': ['*.so*']},  # Include the .so file
)

