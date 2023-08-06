import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="influxdb_wrapper",
    version="0.0.5",
    author="Ismael Raya",
    author_email="phornee@gmail.com",
    description="DB management wrapper over influxDB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Phornee/influxdb_wrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'dnspython==1.16.0',
        'influxdb>=5.3.1',
    ],
    python_requires='>=3.6',
)
