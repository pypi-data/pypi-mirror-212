from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='smart-alpha-connect',
    version='0.0.2',
    description='SmartAlpha Connect',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LunaticFrisbee/smart-alpha-connect",
    author="SmartAlpha",
    author_email="Smartalpha2018@gmail.com",
    py_modules=['SmartAlphaConnect'],
    package_dir={'': 'src'},
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ]
)