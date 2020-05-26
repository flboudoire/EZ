import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="echem-EZ",
    version="1.0.26",
    author="Florent Boudoire",
    author_email="flboudoire@gmail.com",
    description="EZ - Z vs E made easy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/flboudoire/EZ",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
