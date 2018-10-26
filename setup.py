import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ca_img_analyzer",
    version="0.0.2",
    description="""Helper functions that facilitate the analysis
                   of experimental calcium imaging data""",
    license="MIT",
    packages=["ca_img_analyzer"],
    author="Daniel Schuette",
    author_email="d.schuette@online.de",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["Calcium Imaging"],
    url="https://github.com/DanielSchuette/ca_img_analyzer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
