import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-FormulaBasedMaterials", # Replace with your own username
    version="0.0.1",
    author="Michael, Yu-Chuan, Hsu",
    author_email="mk60503mk60503@gmail.com",
    description="A code for generating Formula-Based Materials into Voxel, STL files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MicDonald/FormulaBasedMaterials",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[            # I get to this in a second
        'numpy',
        'matplotlib',
        'trimesh',
        'mpl_toolkits',
        'time',
        'warnings',
        'skimage',
        'random',
        'sympy',
          
      ],
    python_requires='>=3.6',
)