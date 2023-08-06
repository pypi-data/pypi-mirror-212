""" setup """
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="log_mgr",
    version="0.1.1",
    author="Ismael Raya",
    author_email="phornee@gmail.com",
    description="Utility class for logging with handlers included",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Phornee/log_mgr",
    packages=setuptools.find_packages(),
    package_data={
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    ],
    python_requires='>=3.6',
)