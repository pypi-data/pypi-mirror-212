# from setuptools import setup

# setup(
#     name="mi_libreria",
#     version="0.5",
#     py_modules=["mi_libreria"],
#     entry_points={
#         "console_scripts": [
#             "mi_libreria = mi_libreria.__main__:main"
#         ]
#     }
# )

import setuptools

with open("README.md", "r", encoding="utf-8") as ld:
    long_description = ld.read()

setuptools.setup(
    name="Orbus",
    version="1.0.3",
    author="Wilovy09",
    author_email="orbuscompany@gmail.com",
    description="An app skeleton creator, using CLI interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OrbusCompany/Orbus",
    project_url={
        "Bug Tracker": "https://github.com/OrbusCompany/Orbus/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    
    py_modules=["orbusmaker"],
    entry_points={
        "console_scripts": [
            "orbusmaker = orbusmaker.__main__:main"
        ]
    },
    python_requires=">3.10"
)