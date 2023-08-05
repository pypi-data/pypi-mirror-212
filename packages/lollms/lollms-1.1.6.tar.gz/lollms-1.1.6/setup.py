from pathlib import Path
from typing import Union

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def read_requirements(path: Union[str, Path]):
    with open(path, "r") as file:
        return file.read().splitlines()


requirements = read_requirements("requirements.txt")
requirements_dev = read_requirements("requirements_dev.txt")

def get_all_files(path):
    path = Path(path)
    file_list = []
    for file_path in path.rglob('*'):
        if file_path.name!="local_config.yaml" and file_path.name!=".installed" and file_path.name!=".git" and file_path.name!=".gitignore" and file_path.name!=".git" and file_path.name!=".git":
            if file_path.is_file():
                file_list.append("".join(str(file_path).replace("\\","/").split("/")[1:]))
    return file_list

setuptools.setup(
    name="lollms",
    version="1.1.6",
    author="Saifeddine ALOUI",
    author_email="aloui.saifeddine@gmail.com",
    description="A python library for AI personality definition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ParisNeo/lollms",
    packages=setuptools.find_packages(),
    package_data={
        "lollms": [
            "bindings_zoo/*",
            "personalities_zoo/*",
            "assets/*",
            "configs/*"
        ]+get_all_files("lollms/bindings_zoo")
        +get_all_files("lollms/personalities_zoo")
    },
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'lollms-server = lollms.server:main',
        ],
    },
    extras_require={"dev": requirements_dev},
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
