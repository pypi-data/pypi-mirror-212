import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pfizer_components",
    version="0.1.8",
    author="ZS Associates",
    description="Custom Python Dash Components for Pfizer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", #TODO
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["Components"],
    package_data={
        'pfizer_components': ['assets/*.svg','assets/dbc.css','assets/*.PNG']
    }
    # install_requires=['plotly>=5.0.0', 'dash==2.0.0rc2', ] #TODO
)
