import setuptools


setuptools.setup(
    name="img2data", # Replace with your own username
    version="0.0.1",
    author="julmubm",
    author_email="dltpdn@gmail.com",
    description="Divide a number of handwritten digits in one image into individual images.",
    long_description_content_type="text/markdown",
    url="https://github.com/dltpdn/img2data",
    install_requires=['opencv-python', 'numpy'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)