from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="gk_calculator",
    version="1.0.0",
    author="Ahmed Kibria",
    author_email="gkibria121@email.com",
    description="A advanced calculator program",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gkibria121/calculator",
    install_requires=['regex'],
    packages=["gk_calculator"],
    keywords=['python', 'calculator', 'python calculator', 'gk calculator','advanced calculator'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
