from setuptools import setup, find_packages

setup(
    name="ModParameter",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "customtkinter==5.2.2",
        "Pillow==11.1.0",
    ],
    entry_points={
        "console_scripts": [
            "ModParameter = main.main:main"
        ]
    },
)
