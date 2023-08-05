from setuptools import setup, find_packages
import sys

# Determine Python version
python_version = '>=2.7.*' if sys.version_info.major == 2 else '>=3.6'
packages = find_packages()

requirements = [
    'docopt',
]


setup(
    author='Norbert Gocze',
    author_email='gnorbi951@gmail.com',
    version='0.0.1',
    python_requires=python_version,
    description="Utility tool used for parsing specific .ini files",
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='rest_helper',
    name='rest_helper',
    packages=packages,
    install_requires=requirements,
)
