from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = "KitronikPicoZIP96",
    version = "1.0.0",
    description = "Kitronik Pico ZIP96 a complete controller with LED screen",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    py_modules = ["ZIP96Pico"],
)
