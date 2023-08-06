from setuptools import setup


setup(
    name="node-thunder",
    version="0.1.0",
    author="Aradhya Pitlawar",
    author_email="pitlawararadhya@gmail.com",
    description="A script to set up a basic Node.js project",
    long_description_content_type="text/markdown",
    packages=["mynode_setup"],
    scripts=["mynode_setup/__main__.py"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "node-thunder= mynode_setup.__main__:main",
        ],
    },  # Add any dependencies here
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
