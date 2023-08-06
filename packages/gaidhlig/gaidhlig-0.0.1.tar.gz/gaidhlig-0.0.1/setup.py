from setuptools import setup, find_packages


setup(
    name="gaidhlig",
    version="0.0.1",
    license="MIT",
    author="Mike Arpaia",
    author_email="mike@arpaia.co",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/gaidhlig/python",
    keywords="nlp",
    install_requires=[],
)
