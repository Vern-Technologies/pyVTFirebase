import setuptools

with open("pyVTFirebase/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_behrtech",
    version="2021.4.05.2",
    license="MIT",
    author="Matthew Ashley",
    author_email="matthewashley@verntechnologies.com",
    description="A Python wrapper package for the Firebase REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
        'httpx',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)