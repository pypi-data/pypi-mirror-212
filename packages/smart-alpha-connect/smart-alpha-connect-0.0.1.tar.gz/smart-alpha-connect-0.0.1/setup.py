from setuptools import setup

setup(
    name='smart-alpha-connect',
    version='0.0.1',
    description='SmartAlpha Connect',
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