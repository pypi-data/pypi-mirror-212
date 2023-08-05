import setuptools
 
with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="motionsenseapp",
    version="0.0.2",
    author="Cole Hagen",
    author_email="hagencolej@gmail.com",
    description="Motion Sense",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[            # I get to this in a second
          'mediapipe',
          'opencv-python-headless',
          'plotly',
          'pandas',
          'numpy'
      ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)