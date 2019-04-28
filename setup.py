import setuptools

with open('README.md') as readme:
    long_description = readme.read()

setuptools.setup(
    name="asmm",
    version="0.0.1",
    author="Oliver Maskery",
    author_email="omaskery@googlemail.com",
    description="ArmA SQF Module Manager (prototype)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/omaskery/asmm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    entry_points={
        'console_scripts': [
            'asmm=asmm.cli:main'
        ]
    }
)
