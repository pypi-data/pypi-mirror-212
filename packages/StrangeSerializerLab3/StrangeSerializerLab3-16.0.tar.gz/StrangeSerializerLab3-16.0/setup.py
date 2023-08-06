from setuptools import setup, find_packages


setup(
    name="StrangeSerializerLab3",
    version="16.0",
    description="Serializer for lab_3",
    author="Mihail Kornievich",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=["StrangeSerializerLab3", "StrangeSerializerLab3/StrangeJSON", "StrangeSerializerLab3/StrangeXML"],
    include_package_data=True
)