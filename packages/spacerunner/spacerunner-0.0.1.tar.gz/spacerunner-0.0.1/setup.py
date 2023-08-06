# Lint as: python3
# pylint: enable=line-too-long

from setuptools import find_packages, setup


with open("README.md") as f:
    long_description = f.read()


if __name__ == "__main__":
    setup(
        name="spacerunner",
        description="spacerunner",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Abhishek Thakur",
        url="https://github.com/abhishekkrthakur/spacerunner",
        license="Apache License",
        packages=find_packages(),
        version="0.0.1",
        include_package_data=True,
        platforms=["linux", "unix"],
        python_requires=">=3.8",
        classifiers=[
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.8",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
        ],
    )
