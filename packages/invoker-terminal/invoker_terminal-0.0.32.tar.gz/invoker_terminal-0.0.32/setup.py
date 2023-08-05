"""Python setup.py for invoker_terminal package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("invoker_terminal", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="invoker_terminal",
    version=read("invoker_terminal", "VERSION"),
    description="Awesome invoker_terminal created by m00dy",
    url="https://github.com/m00dy/invoker-terminal/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="m00dy",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["invoker_terminal = invoker_terminal.__main__:main"]
    },
    extras_require={"test": read_requirements("requirements-test.txt")},
    include_package_data=True
)
