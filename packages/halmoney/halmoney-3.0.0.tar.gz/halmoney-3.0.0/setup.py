# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
#with open("README.md", "rt", encoding='UTF8') as fh:
#    long_description = fh.read()
setup(
    name='halmoney',
    version='3.0.0',
    url='https://github.com/sjpark/halmoney',
    download_url='https://github.com/sjpark/halmoney/archive/v3.0.0.tar.gz',
    author='sjpark',
    author_email='sjpkorea@yahoo.com',
    description='Easy Read / Write for Excel, Word, Color, Etc using Python',
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "halmoney": ["*.*"],
        },
    long_description_content_type="text/markdown",
    long_description=open('README.md', "r", encoding='UTF8').read(),
    install_requires=[''],
    python_requires='>=3.5',
    zip_safe=False,
    classifiers=['License :: OSI Approved :: MIT License'],
    )