from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent


setup(
    name='ordinal_number',
    version='0.2',
    packages=find_packages(),
    author_email="alphagameplayerpro@gmail.com",
    license="MIT",
    description="A package to use OrdinnalNumber",
    long_description = (this_directory / "README.md").read_text(),
    long_description_content_type='text/plain',
    url='https://github.com/OrdinalNumber/ordinal'
)