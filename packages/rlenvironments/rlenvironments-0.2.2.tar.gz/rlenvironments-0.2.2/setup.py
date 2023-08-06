import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rlenvironments",
    version="0.2.2",
    author="Umut Koksoy",
    author_email="umutkoksoy@gmail.com",
    description="Python library for target seeking environment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ukoksoy/rlenvironments",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="reinforcement-learning environment target-seeking",
    install_requires=[
        "numpy",
        "matplotlib"
    ],
    python_requires=">=3.7",
)
