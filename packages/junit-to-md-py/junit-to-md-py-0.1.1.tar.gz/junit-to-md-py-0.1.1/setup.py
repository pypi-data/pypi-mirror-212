from setuptools import setup, find_packages

setup(
    name="junit-to-md-py",
    version="0.1.1",
    author="srydz_catalogicsoftware",
    author_email="srydz@catalogicsoftware.com",
    description="Python script which converts junit xml file/text into the markdown representation",
    long_description=open("README.md").read(),
    url='https://github.com/catalogicsoftware/dpx-utils-junit-to-md',
    license='MIT',
    packages=["script"],
    install_requires=[
        "lxml",
    ],
)
